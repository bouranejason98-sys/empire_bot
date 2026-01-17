import makeWASocket, { DisconnectReason, useMultiFileAuthState, fetchLatestBaileysVersion } from "@whiskeysockets/baileys";
import qrcode from "qrcode-terminal";
import axios from "axios";
import https from "https";

async function startBailey() {
  const { state, saveCreds } = await useMultiFileAuthState("auth_info");
  const { version } = await fetchLatestBaileysVersion();

  const agent = new https.Agent({ family: 4 });

  const sock = makeWASocket({
    version,
    auth: state,
    fetchAgent: agent,
    browser: ["Ubuntu","Chrome","120.0"],
    connectTimeoutMs: 60000,
    defaultQueryTimeoutMs: 60000
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", (update) => {
    const { connection, qr, lastDisconnect } = update;
    if (qr) {
      qrcode.generate(qr,{small:true});
      console.log("📱 Scan this QR code with WhatsApp");
    }
    if (connection === "open") console.log("✅ WhatsApp connected successfully!");
    if (connection === "close") {
      const shouldReconnect = (lastDisconnect?.error?.output?.statusCode ?? 0) !== DisconnectReason.loggedOut;
      console.log("❌ Connection closed. Reconnecting:", shouldReconnect);
      if (shouldReconnect) setTimeout(startBailey,5000);
    }
  });

  sock.ev.on("messages.upsert", async (m) => {
    const msg = m.messages[0];
    if (!msg.message || msg.key.fromMe) return;

    const sender = msg.key.remoteJid;
    const text = msg.message.conversation || msg.message.extendedTextMessage?.text || "";

    console.log("📩 Incoming:", sender, text);

    try {
      const res = await axios.post("http://localhost:8000/handle", {
        user: sender,
        message: text,
        clone: {id:"kenya_real_estate",region:"Kenya"}
      });
      const reply = res.data.reply || "⚠️ No reply generated";
      await sock.sendMessage(sender,{text:reply});
    } catch(err){
      console.error("Empire Gateway error:",err.message);
      await sock.sendMessage(sender,{text:"⚠️ System temporarily unavailable."});
    }
  });
}

startBailey();
