import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, time

cache = {}
CACHE_DURATION = 21600

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Blue$Leaf8Run")
CAMS_FILE = "cams.json"

def load_cams():
    if os.path.exists(CAMS_FILE):
        with open(CAMS_FILE, "r") as f:
            return json.load(f)
    return []

def save_cams(cams):
    with open(CAMS_FILE, "w") as f:
        json.dump(cams, f, indent=2)

def get_default_cams():
    return [
    {"id": "1", "name": "Narvik Havn", "location": "Norway", "videoId": "HCslThfpWqk", "directUrl": "", "timezone": "Europe/Oslo", "lat": 68.4385, "lon": 17.4279, "category": "Europe", "thumbnailOverride": ""},
    {"id": "2", "name": "Geiranger", "location": "Norway", "videoId": "wAdTV6Uc5eA", "directUrl": "", "timezone": "Europe/Oslo", "lat": 62.1003, "lon": 7.2058, "category": "Europe", "thumbnailOverride": ""},
    {"id": "3", "name": "The Temple Bar", "location": "Dublin, Ireland", "videoId": "3nyPER2kzqk", "directUrl": "", "timezone": "Europe/Dublin", "lat": 53.3453, "lon": -6.2678, "category": "Europe", "thumbnailOverride": ""},
    {"id": "4", "name": "Ponte delle Guglie", "location": "Venice, Italy", "videoId": "mt7uE-n0YPI", "directUrl": "", "timezone": "Europe/Rome", "lat": 45.4408, "lon": 12.3155, "category": "Europe", "thumbnailOverride": ""},
    {"id": "5", "name": "Soggy Dollar", "location": "British Virgin Island, Caribbean", "videoId": "V_I168MM-ik", "directUrl": "", "timezone": "America/Tortola", "lat": 18.4655, "lon": -64.5234, "category": "Caribbean", "thumbnailOverride": ""},
    {"id": "6", "name": "Bryant Park", "location": "New York, USA", "videoId": "JPxiYF2fSC8", "directUrl": "", "timezone": "America/New_York", "lat": 40.7536, "lon": -73.9832, "category": "USA", "thumbnailOverride": ""},
    {"id": "7", "name": "Port Miami Cruise Ship", "location": "Miami, USA", "videoId": "9iV-D-KAtao", "directUrl": "", "timezone": "America/New_York", "lat": 25.7742, "lon": -80.17, "category": "USA", "thumbnailOverride": ""},
    {"id": "8", "name": "Jacksonville Beach", "location": "Jacksonville, Florida", "videoId": "JLvCEDGJr-s", "directUrl": "", "timezone": "America/New_York", "lat": 30.2919, "lon": -81.393, "category": "USA", "thumbnailOverride": ""},
    {"id": "9", "name": "Jackson Hole Town Square", "location": "Jackson Hole, Wyoming", "videoId": "1EiC9bvVGnk", "directUrl": "", "timezone": "America/Denver", "lat": 43.4799, "lon": -110.7624, "category": "USA", "thumbnailOverride": ""},
    {"id": "10", "name": "Jackson Hole Town Square-Northeast", "location": "Jackson Hole, Wyoming", "videoId": "Zj0pXlq2-jI", "directUrl": "", "timezone": "America/Denver", "lat": 43.4799, "lon": -110.7624, "category": "USA", "thumbnailOverride": ""},
    {"id": "11", "name": "Rolling Cam Venice", "location": "Venice, Italy", "videoId": "a1mcaV3Sf9U", "directUrl": "", "timezone": "Europe/Rome", "lat": 45.4408, "lon": 12.3155, "category": "Europe", "thumbnailOverride": ""},
    {"id": "12", "name": "Sydney Harbor", "location": "Sydney, Australia", "videoId": "5uZa3-RMFos", "directUrl": "", "timezone": "Australia/Sydney", "lat": -33.8688, "lon": 151.2093, "category": "Asia Pacific", "thumbnailOverride": ""},
    {"id": "13", "name": "New River Cam", "location": "Fort Lauderdale, Florida", "videoId": "3LtOF19QGQY", "directUrl": "", "timezone": "America/New_York", "lat": 26.1224, "lon": -80.1373, "category": "USA", "thumbnailOverride": ""},
    {"id": "14", "name": "Venice Beach", "location": "Venice Beach, California", "videoId": "EO_1LWqsCNE", "directUrl": "", "timezone": "America/Los_Angeles", "lat": 33.985, "lon": -118.4695, "category": "USA", "thumbnailOverride": ""},
    {"id": "15", "name": "Sag Harbor Hamptons", "location": "Sag Harbor Village, New York", "videoId": "sxZxz0OPoh0", "directUrl": "", "timezone": "America/New_York", "lat": 40.9998, "lon": -72.2948, "category": "USA", "thumbnailOverride": ""},
    {"id": "16", "name": "St. George Street South", "location": "St Augustine", "videoId": "ZksWoEAhmTU", "directUrl": "", "timezone": "America/New_York", "lat": 29.8947, "lon": -81.3145, "category": "USA", "thumbnailOverride": ""},
    {"id": "17", "name": "Duval Street Cam", "location": "Key West, Florida", "videoId": "BP9AtblEpXE", "directUrl": "", "timezone": "America/New_York", "lat": 24.5551, "lon": -81.78, "category": "USA", "thumbnailOverride": ""},
    {"id": "18", "name": "Winter Garden", "location": "Winter Garden, Florida", "videoId": "sKcmQQqzQcM", "directUrl": "", "timezone": "America/New_York", "lat": 28.5653, "lon": -81.5862, "category": "USA", "thumbnailOverride": ""},
    {"id": "19", "name": "Jupiter Reef Club", "location": "Jupiter, Florida", "videoId": "1FYgBpkM7SA", "directUrl": "", "timezone": "America/New_York", "lat": 26.9342, "lon": -80.0942, "category": "USA", "thumbnailOverride": ""},
    {"id": "20", "name": "Market Square West", "location": "Newburyport, Massachusetts", "videoId": "VsuSbXPN93o", "directUrl": "", "timezone": "America/New_York", "lat": 42.8126, "lon": -70.8773, "category": "USA", "thumbnailOverride": ""},
    {"id": "21", "name": "Whale Watch Cam", "location": "Maui, Hawaii, USA", "videoId": "qBoQP57ExPI", "directUrl": "", "timezone": "Pacific/Honolulu", "lat": 20.7984, "lon": -156.3319, "category": "USA", "thumbnailOverride": ""},
    {"id": "22", "name": "Bay View", "location": "San Francisco, California", "videoId": "BSWhGNXxT9A", "directUrl": "", "timezone": "America/Los_Angeles", "lat": 37.7749, "lon": -122.4194, "category": "USA", "thumbnailOverride": ""},
    {"id": "23", "name": "New York City Skyline", "location": "New York City, New York", "videoId": "tojOBePB2f4", "directUrl": "", "timezone": "America/New_York", "lat": 40.7128, "lon": -74.006, "category": "USA", "thumbnailOverride": ""},
    {"id": "24", "name": "Leavenworth", "location": "Leavenworth, Washington", "videoId": "TmtVbezZaqg", "directUrl": "", "timezone": "America/Los_Angeles", "lat": 47.5963, "lon": -120.6615, "category": "USA", "thumbnailOverride": ""},
    {"id": "25", "name": "Los Angeles Airport", "location": "Los Angeles, California", "videoId": "hFYlgU-1eRE", "directUrl": "", "timezone": "America/Los_Angeles", "lat": 33.9425, "lon": -118.4081, "category": "USA", "thumbnailOverride": ""},
    {"id": "26", "name": "Main Beach", "location": "East Hampton Village, New York", "videoId": "yLU8DNeXXmc", "directUrl": "", "timezone": "America/New_York", "lat": 40.9621, "lon": -72.1848, "category": "USA", "thumbnailOverride": ""},
    {"id": "27", "name": "Windmill Bar Jam Fam Cam", "location": "St. John, USVI", "videoId": "d-drfinzIWU", "directUrl": "", "timezone": "America/St_Thomas", "lat": 18.3333, "lon": -64.7333, "category": "Caribbean", "thumbnailOverride": ""},
    {"id": "28", "name": "Cruz Bay Beach Cam", "location": "St. John, USVI", "videoId": "ZQ5OqjssArE", "directUrl": "", "timezone": "America/St_Thomas", "lat": 18.33, "lon": -64.7967, "category": "Caribbean", "thumbnailOverride": ""},
    {"id": "29", "name": "Main Street", "location": "Breckenridge, Colorado", "videoId": "SH63YaIWyK0", "directUrl": "", "timezone": "America/Denver", "lat": 39.4817, "lon": -106.0384, "category": "USA", "thumbnailOverride": ""},
    {"id": "30", "name": "Yellowstone National Park", "location": "Wyoming", "videoId": "A0kI9N5mk-4", "directUrl": "", "timezone": "America/Denver", "lat": 44.428, "lon": -110.5885, "category": "USA", "thumbnailOverride": ""},
    {"id": "31", "name": "Boardwalk", "location": "Atlantic City, New Jersey", "videoId": "vVyBOU9Huvo", "directUrl": "", "timezone": "America/New_York", "lat": 39.3643, "lon": -74.4229, "category": "USA", "thumbnailOverride": ""},
    {"id": "32", "name": "Lower Main Street", "location": "Nantucket, Massachusetts", "videoId": "sp-FHZY95QM", "directUrl": "", "timezone": "America/New_York", "lat": 41.2835, "lon": -70.0995, "category": "USA", "thumbnailOverride": ""},
    {"id": "33", "name": "Pelican Beach", "location": "Destin, Florida", "videoId": "sS4GzzSOY8Q", "directUrl": "", "timezone": "America/Chicago", "lat": 30.3935, "lon": -86.4958, "category": "USA", "thumbnailOverride": ""},
    {"id": "34", "name": "Holden Beach", "location": "North Carolina", "videoId": "sBtvpwKH2BE", "directUrl": "", "timezone": "America/New_York", "lat": 33.9099, "lon": -78.2717, "category": "USA", "thumbnailOverride": ""},
    {"id": "35", "name": "Leavenworth Downtown", "location": "Leavenworth, Washington", "videoId": "XjhxRZEm638", "directUrl": "", "timezone": "America/Los_Angeles", "lat": 47.5963, "lon": -120.6615, "category": "USA", "thumbnailOverride": ""},
    {"id": "36", "name": "Jimmy Fish House", "location": "Clearwater, Florida", "videoId": "9c1oLjB3wIs", "directUrl": "", "timezone": "America/New_York", "lat": 27.9659, "lon": -82.8001, "category": "USA", "thumbnailOverride": ""},
    {"id": "37", "name": "Miami River", "location": "Miami, Florida", "videoId": "7wHgYc_kN98", "directUrl": "", "timezone": "America/New_York", "lat": 25.7742, "lon": -80.1936, "category": "USA", "thumbnailOverride": ""},
    {"id": "38", "name": "Navarre Beach Pier", "location": "Navarre Beach, Florida", "videoId": "7WzKQETomHU", "directUrl": "", "timezone": "America/Chicago", "lat": 30.3766, "lon": -86.8628, "category": "USA", "thumbnailOverride": ""},
    {"id": "39", "name": "Biscayne Bay", "location": "Miami, Florida", "videoId": "4UzQd1dVPlo", "directUrl": "", "timezone": "America/New_York", "lat": 25.7617, "lon": -80.1918, "category": "USA", "thumbnailOverride": ""},
    {"id": "40", "name": "Grimentz", "location": "Valais, Switzerland", "videoId": "iCxfe27HpaY", "directUrl": "", "timezone": "Europe/Zurich", "lat": 46.1833, "lon": 7.5833, "category": "Europe", "thumbnailOverride": ""},
    {"id": "41", "name": "Pensacola Beach", "location": "Pensacola, Florida", "videoId": "2X0GdFzfv3A", "directUrl": "", "timezone": "America/Chicago", "lat": 30.3366, "lon": -87.1569, "category": "USA", "thumbnailOverride": ""},
    {"id": "42", "name": "Lawai Beach", "location": "Kauai, Hawaii", "videoId": "3ATYHKN2hIg", "directUrl": "", "timezone": "Pacific/Honolulu", "lat": 21.8951, "lon": -159.5183, "category": "USA", "thumbnailOverride": ""},
    {"id": "43", "name": "Washington Monument", "location": "Washington DC", "videoId": "oDCAAfOSqvA", "directUrl": "", "timezone": "America/New_York", "lat": 38.8895, "lon": -77.0353, "category": "USA", "thumbnailOverride": ""},
    {"id": "44", "name": "Napili Sunset Beachfront", "location": "Maui, Hawaii", "videoId": "GL_2CrLwSDA", "directUrl": "", "timezone": "Pacific/Honolulu", "lat": 20.9976, "lon": -156.6665, "category": "USA", "thumbnailOverride": ""},
    {"id": "45", "name": "Klein Curaçao", "location": "Curaçao, Caribbean", "videoId": "_P3fgFEG55E", "directUrl": "", "timezone": "America/Curacao", "lat": 11.9833, "lon": -68.6333, "category": "Caribbean", "thumbnailOverride": ""},
    {"id": "46", "name": "Deerfield Beach", "location": "Deerfield Beach, Florida", "videoId": "rdeoEeJ00xA", "directUrl": "", "timezone": "America/New_York", "lat": 26.3184, "lon": -80.0998, "category": "USA", "thumbnailOverride": ""},
    {"id": "47", "name": "Sunset Grille", "location": "Florida Keys, Florida", "videoId": "SXMC-MzSncI", "directUrl": "", "timezone": "America/New_York", "lat": 24.7136, "lon": -81.0998, "category": "USA", "thumbnailOverride": ""},
    {"id": "48", "name": "Gatlinburg Skypark", "location": "Gatlinburg, Tennessee", "videoId": "Exaxsl-pg84", "directUrl": "", "timezone": "America/New_York", "lat": 35.7143, "lon": -83.5102, "category": "USA", "thumbnailOverride": ""},
    {"id": "49", "name": "Oudeschild Harbour", "location": "Texel Island, Netherlands", "videoId": "NYGtSbvt6d0", "directUrl": "", "timezone": "Europe/Amsterdam", "lat": 53.0444, "lon": 4.8566, "category": "Europe", "thumbnailOverride": ""},
    {"id": "50", "name": "Boardwalk Cam", "location": "Philipsburg, Saint Martin", "videoId": "N5Mb2bjYwZo", "directUrl": "", "timezone": "America/Lower_Princes", "lat": 18.0236, "lon": -63.0458, "category": "Caribbean", "thumbnailOverride": ""},
    {"id": "51", "name": "Fishing Pier Cam", "location": "Deerfield Beach, Florida", "videoId": "H33wtprQqSM", "directUrl": "", "timezone": "America/New_York", "lat": 26.3184, "lon": -80.0998, "category": "USA", "thumbnailOverride": ""},
    {"id": "52", "name": "Sunset Terrace", "location": "Fort Myers Beach, Florida", "videoId": "2qd9j2CbIpg", "directUrl": "", "timezone": "America/New_York", "lat": 26.4518, "lon": -81.9479, "category": "USA", "thumbnailOverride": ""},
    {"id": "53", "name": "Curacao World Heritage", "location": "Willemstad, Curaçao", "videoId": "28U-t3fA9ks", "directUrl": "", "timezone": "America/Curacao", "lat": 12.1084, "lon": -68.9335, "category": "Caribbean", "thumbnailOverride": ""},
    {"id": "54", "name": "Bourbon Street Balcony", "location": "New Orleans, Louisiana", "videoId": "C32EiZiQPkQ", "directUrl": "", "timezone": "America/Chicago", "lat": 29.9584, "lon": -90.0653, "category": "USA", "thumbnailOverride": ""},
    {"id": "55", "name": "Bourbon Street View", "location": "New Orleans, Louisiana", "videoId": "Ksrleaxxxhw", "directUrl": "", "timezone": "America/Chicago", "lat": 29.9584, "lon": -90.0653, "category": "USA", "thumbnailOverride": ""},
    {"id": "56", "name": "St. Augustine Alligator Farm", "location": "St. Augustine, Florida", "videoId": "LHtzZf4T7xw", "directUrl": "", "timezone": "America/New_York", "lat": 29.8938, "lon": -81.3108, "category": "USA", "thumbnailOverride": ""},
    {"id": "57", "name": "Robbie's Marina", "location": "Islamorada, Florida Keys", "videoId": "awTeFw1hPp4", "directUrl": "", "timezone": "America/New_York", "lat": 24.9087, "lon": -80.6248, "category": "USA", "thumbnailOverride": ""},
    {"id": "58", "name": "Chapel Bridge", "location": "Lucerne, Switzerland", "videoId": "QIt1FaDMnQc", "directUrl": "", "timezone": "Europe/Zurich", "lat": 47.0502, "lon": 8.3093, "category": "Europe", "thumbnailOverride": ""},
    {"id": "59", "name": "Tora Beach", "location": "Paguera, Mallorca, Spain", "videoId": "Pgjsoeq7iGM", "directUrl": "", "timezone": "Europe/Madrid", "lat": 39.5391, "lon": 2.4597, "category": "Europe", "thumbnailOverride": ""},
    {"id": "60", "name": "House of Sunset", "location": "Port d'Andratx, Mallorca, Spain", "videoId": "RPTEW6-Dau0", "directUrl": "", "timezone": "Europe/Madrid", "lat": 39.5333, "lon": 2.3833, "category": "Europe", "thumbnailOverride": ""},
    {"id": "61", "name": "Sant Elm Beach", "location": "Sant Elm, Mallorca, Spain", "videoId": "9svQ7gvPGc0", "directUrl": "", "timezone": "Europe/Madrid", "lat": 39.5833, "lon": 2.35, "category": "Europe", "thumbnailOverride": ""},
    {"id": "62", "name": "Vervet", "location": "Tromso, Norway", "videoId": "3y7_fkAzzps", "directUrl": "", "timezone": "Europe/Oslo", "lat": 69.6492, "lon": 18.9553, "category": "Europe", "thumbnailOverride": ""},
    {"id": "63", "name": "Rittenhouse Square", "location": "Philadelphia, Pennsylvania", "videoId": "1vGH-8jvKcg", "directUrl": "", "timezone": "America/New_York", "lat": 39.9496, "lon": -75.1715, "category": "USA", "thumbnailOverride": ""},
    {"id": "64", "name": "Harbor Cam", "location": "New York City, New York", "videoId": "", "directUrl": "https://cdn77.ptztv.live/eUBVKlrSqtUjJe_sM7wdiw==,1780901263/cdnorigin/nyhwmux.stream/chunklist_DVR.m3u8", "timezone": "America/New_York", "lat": 40.7128, "lon": -74.006, "category": "USA", "thumbnailOverride": "https://i.imgur.com/rXoM42Q.png"}
]

if not os.path.exists(CAMS_FILE):
    save_cams(get_default_cams())

ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Camzy Admin</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { height: 100%; }
        body { font-family: Arial, sans-serif; background: #0d1b2a; color: white; }
        .page { padding: 20px; padding-bottom: 40px; }
        h1 { color: #4a9eff; margin-bottom: 20px; }
        h2 { color: #4a9eff; margin-bottom: 15px; }
        .cam-list { margin-bottom: 30px; }
        .cam-item { background: #1a2a3a; padding: 12px; margin-bottom: 8px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .cam-name { font-weight: bold; }
        .cam-location { color: #4a9eff; font-size: 12px; }
        .cam-category { color: #888; font-size: 12px; }
        .delete-btn { background: #ff4444; border: none; color: white; padding: 6px 12px; border-radius: 4px; cursor: pointer; touch-action: manipulation; }
        .edit-btn { background: #4a9eff; border: none; color: white; padding: 6px 12px; border-radius: 4px; cursor: pointer; touch-action: manipulation; }
        .add-form { background: #1a2a3a; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .form-group { margin-bottom: 12px; }
        label { display: block; margin-bottom: 4px; font-size: 14px; color: #aaa; }
        input, select { width: 100%; padding: 10px; background: #0d1b2a; border: 1px solid #333; color: white; border-radius: 4px; font-size: 16px; }
        input::placeholder { color: #555; }
        .btn { border: none; color: white; padding: 14px; border-radius: 4px; cursor: pointer; touch-action: manipulation; width: 100%; font-size: 16px; margin-top: 8px; display: block; }
        .btn-blue { background: #4a9eff; }
        .btn-grey { background: #555; }
        .btn-back { background: #1a2a3a; margin-bottom: 15px; width: auto; padding: 10px 16px; display: inline-block; }
        .action-btns { background: #0d1b2a; padding: 10px 0; margin-bottom: 15px; }
        .login-form { max-width: 300px; margin: 100px auto; background: #1a2a3a; padding: 30px; border-radius: 8px; }
        .msg { padding: 10px; border-radius: 4px; margin-bottom: 15px; text-align: center; }
        .error { background: #4a1a1a; color: #ff4a4a; }
    </style>
</head>
<body>
    <div id="app"></div>
    <script>
        let authed = false;
        let cams = [];
        let editingId = null;
        let view = 'login';

        function render() {
            if (view === 'login') renderLogin();
            else if (view === 'list') renderList();
            else if (view === 'edit') renderEdit();
            else if (view === 'add') renderAdd();
        }

        function renderLogin() {
            document.getElementById('app').innerHTML = `
                <div class="login-form">
                    <h2>Camzy Admin</h2>
                    <div class="form-group">
                        <label>Password</label>
                        <input type="password" id="pwd" placeholder="Enter password" />
                    </div>
                    <button class="btn btn-blue" onclick="login()">Login</button>
                    <div id="login-msg"></div>
                </div>`;
        }

        function login() {
            const pwd = document.getElementById('pwd').value;
            fetch('/admin/verify', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({password: pwd})
            }).then(r => r.json()).then(d => {
                if (d.ok) {
                    authed = true;
                    window._pwd = pwd;
                    loadCams();
                } else {
                    document.getElementById('login-msg').innerHTML = '<div class="msg error">Wrong password!</div>';
                }
            });
        }

        function loadCams() {
            fetch('/cams').then(r => r.json()).then(data => {
                cams = data;
                view = 'list';
                render();
            });
        }

        function renderList() {
            document.getElementById('app').innerHTML = `
                <div class="page">
                    <h1>Camzy Admin</h1>
                    <input type="search" id="search-box" placeholder="Search cams..." oninput="filterCams()" style="margin-bottom:15px;background:#1a2a3a;border:1px solid #4a9eff;" />
                    <div class="cam-list">
                        <h2>Cams (${cams.length})</h2>
                        ${cams.map(cam => `
                            <div class="cam-item">
                                <div style="flex:1">
                                    <div class="cam-name">${cam.name}</div>
                                    <div class="cam-location">${cam.location}</div>
                                    <div class="cam-category">${cam.category}</div>
                                </div>
                                <div style="display:flex;gap:8px;">
                                    <button class="edit-btn" onclick="showEdit('${cam.id}')">Edit</button>
                                    <button class="delete-btn" onclick="deleteCam('${cam.id}')">Delete</button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    <button class="btn btn-blue" onclick="showAdd()">+ Add New Cam</button>
                </div>`;
            window.scrollTo(0, 0);
        }

        function showEdit(id) {
            editingId = id;
            view = 'edit';
            render();
            window.scrollTo(0, 0);
        }

        function showAdd() {
            view = 'add';
            render();
            window.scrollTo(0, 0);
        }

        function renderEdit() {
            const cam = cams.find(c => c.id === editingId);
            document.getElementById('app').innerHTML = `
                <div class="page">
                    <div class="action-btns">
                        <button class="btn btn-blue" onclick="saveCam()">Save</button>
                        <button class="btn btn-grey" onclick="backToList()">Cancel</button>
                    </div>
                    <h2>Edit Cam</h2>
                    <div class="add-form">
                        <div class="form-group"><label>Name</label><input id="e-name" value="${cam.name}" /></div>
                        <div class="form-group"><label>Location</label><input id="e-location" value="${cam.location}" /></div>
                        <div class="form-group"><label>YouTube Video ID</label><input id="e-videoId" value="${cam.videoId}" /></div>
                        <div class="form-group"><label>Direct URL (optional)</label><input id="e-directUrl" value="${cam.directUrl || ''}" /></div>
                        <div class="form-group"><label>Timezone</label><input id="e-timezone" value="${cam.timezone}" /></div>
                        <div class="form-group"><label>Latitude</label><input id="e-lat" value="${cam.lat}" /></div>
                        <div class="form-group"><label>Longitude</label><input id="e-lon" value="${cam.lon}" /></div>
                        <div class="form-group">
                            <label>Category</label>
                            <select id="e-category">
                                <option ${cam.category === 'USA' ? 'selected' : ''}>USA</option>
                                <option ${cam.category === 'Europe' ? 'selected' : ''}>Europe</option>
                                <option ${cam.category === 'Caribbean' ? 'selected' : ''}>Caribbean</option>
                                <option ${cam.category === 'Asia Pacific' ? 'selected' : ''}>Asia Pacific</option>
                            </select>
                        </div>
                        <div class="form-group"><label>Thumbnail URL (optional)</label><input id="e-thumbnail" value="${cam.thumbnailOverride || ''}" /></div>
                    </div>
                </div>`;
            window.scrollTo(0, 0);
        }

        function renderAdd() {
            document.getElementById('app').innerHTML = `
                <div class="page">
                    <div class="action-btns">
                        <button class="btn btn-blue" onclick="addCam()">Add Cam</button>
                        <button class="btn btn-grey" onclick="backToList()">Cancel</button>
                    </div>
                    <h2>Add New Cam</h2>
                    <div class="add-form">
                        <div class="form-group"><label>Name</label><input id="f-name" placeholder="Enter cam name" /></div>
                        <div class="form-group"><label>Location</label><input id="f-location" placeholder="Enter location" /></div>
                        <div class="form-group"><label>YouTube Video ID</label><input id="f-videoId" placeholder="e.g. ABC123xyz" /></div>
                        <div class="form-group"><label>Direct URL (optional)</label><input id="f-directUrl" placeholder="https://..." /></div>
                        <div class="form-group"><label>Timezone</label><input id="f-timezone" placeholder="e.g. America/New_York" /></div>
                        <div class="form-group"><label>Latitude</label><input id="f-lat" placeholder="e.g. 40.7128" /></div>
                        <div class="form-group"><label>Longitude</label><input id="f-lon" placeholder="e.g. -74.0060" /></div>
                        <div class="form-group">
                            <label>Category</label>
                            <select id="f-category">
                                <option>USA</option>
                                <option>Europe</option>
                                <option>Caribbean</option>
                                <option>Asia Pacific</option>
                            </select>
                        </div>
                        <div class="form-group"><label>Thumbnail URL (optional)</label><input id="f-thumbnail" placeholder="https://..." /></div>
                    </div>
                </div>`;
            window.scrollTo(0, 0);
        }

        function backToList() {
            editingId = null;
            view = 'list';
            render();
        }

        function saveCam() {
            const cam = {
                name: document.getElementById('e-name').value,
                location: document.getElementById('e-location').value,
                videoId: document.getElementById('e-videoId').value,
                directUrl: document.getElementById('e-directUrl').value,
                timezone: document.getElementById('e-timezone').value,
                lat: parseFloat(document.getElementById('e-lat').value) || 0,
                lon: parseFloat(document.getElementById('e-lon').value) || 0,
                category: document.getElementById('e-category').value,
                thumbnailOverride: document.getElementById('e-thumbnail').value
            };
            fetch('/cams/' + editingId, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json', 'X-Password': window._pwd},
                body: JSON.stringify(cam)
            }).then(r => r.json()).then(d => {
                if (d.ok) { loadCams(); }
            });
        }

        function deleteCam(id) {
            if (!confirm('Delete this cam?')) return;
            fetch('/cams/' + id, {
                method: 'DELETE',
                headers: {'X-Password': window._pwd}
            }).then(r => r.json()).then(d => {
                if (d.ok) { loadCams(); }
            });
        }

        function addCam() {
            const cam = {
                name: document.getElementById('f-name').value,
                location: document.getElementById('f-location').value,
                videoId: document.getElementById('f-videoId').value,
                directUrl: document.getElementById('f-directUrl').value,
                timezone: document.getElementById('f-timezone').value,
                lat: parseFloat(document.getElementById('f-lat').value) || 0,
                lon: parseFloat(document.getElementById('f-lon').value) || 0,
                category: document.getElementById('f-category').value,
                thumbnailOverride: document.getElementById('f-thumbnail').value
            };
            fetch('/cams', {
                method: 'POST',
                headers: {'Content-Type': 'application/json', 'X-Password': window._pwd},
                body: JSON.stringify(cam)
            }).then(r => r.json()).then(d => {
                if (d.ok) { loadCams(); }
            });
        }

           function filterCams() {
               const query = document.getElementById('search-box').value.toLowerCase();
               const items = document.querySelectorAll('.cam-item');
               items.forEach(item => {
                   const name = item.querySelector('.cam-name').textContent.toLowerCase();
                   const location = item.querySelector('.cam-location').textContent.toLowerCase();
                   item.style.display = (name.includes(query) || location.includes(query)) ? 'flex' : 'none';
            });
        }

        render();
    </script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip("/")

        if path == "admin":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(ADMIN_HTML.encode())
            return

        if path == "cams":
            cams = load_cams()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(cams).encode())
            return

        video_id = path
        if video_id in cache:
            url, timestamp = cache[video_id]
            if time.time() - timestamp < CACHE_DURATION:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"url": url}).encode())
                print(f"Cache hit: {video_id}")
                return

        clients = ["android"]
        url = ""
        for client in clients:
            result = subprocess.run(
                ["yt-dlp", "-g", "--format", "best[ext=mp4]/best",
                 "--extractor-args", f"youtube:player_client={client}",
                 "--no-check-certificate",
                 "--no-playlist",
                 #"--proxy", "http://uriscazf-us-30:b6ivosu9en7i@p.webshare.io:80",
                 "https://www.youtube.com/watch?v=" + video_id],
                capture_output=True, text=True, timeout=30
            )
            url = result.stdout.strip().split("\n")[0]
            if url:
                print(f"Success with client: {client}")
                cache[video_id] = (url, time.time())
                break

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"url": url}).encode())
        print(f"Served: {video_id} -> {url[:80] if url else 'EMPTY'}")

    def do_POST(self):
        path = self.path.strip("/")

        if path == "admin/verify":
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            ok = body.get("password") == ADMIN_PASSWORD
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": ok}).encode())
            return

        if path == "cams":
            if self.headers.get("X-Password") != ADMIN_PASSWORD:
                self.send_response(403)
                self.end_headers()
                return
            length = int(self.headers.get('Content-Length', 0))
            cam = json.loads(self.rfile.read(length))
            cams = load_cams()
            cam["id"] = str(int(time.time()))
            cams.append(cam)
            save_cams(cams)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
            return

    def do_PUT(self):
        path = self.path.strip("/")
        if path.startswith("cams/"):
            if self.headers.get("X-Password") != ADMIN_PASSWORD:
                self.send_response(403)
                self.end_headers()
                return
            cam_id = path.split("/")[1]
            length = int(self.headers.get('Content-Length', 0))
            updated = json.loads(self.rfile.read(length))
            cams = load_cams()
            for i, cam in enumerate(cams):
                if cam["id"] == cam_id:
                    updated["id"] = cam_id
                    cams[i] = updated
                    break
            save_cams(cams)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
            return

    def do_DELETE(self):
        path = self.path.strip("/")
        if path.startswith("cams/"):
            if self.headers.get("X-Password") != ADMIN_PASSWORD:
                self.send_response(403)
                self.end_headers()
                return
            cam_id = path.split("/")[1]
            cams = load_cams()
            cams = [c for c in cams if c["id"] != cam_id]
            save_cams(cams)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
            return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Password")
        self.end_headers()

    def log_message(self, format, *args):
        print(format % args)

port = int(os.environ.get("PORT", 8888))
print(f"Starting server on port {port}")
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
