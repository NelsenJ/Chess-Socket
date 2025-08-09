// Room socket + canvas drag logic
const socket = io();
let canvas = document.getElementById('gameCanvas');
let ctx = canvas.getContext('2d');

let localSID = null; // socket id will be provided by server events (we'll use request.sid server-side)
let circles = {}; // sid -> {x,y,r,color,owner}
let dragging = false;
let dragSid = null;
let offset = {x:0,y:0};

// helper draw
function drawAll(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  for (const [sid, c] of Object.entries(circles)){
    ctx.beginPath();
    ctx.fillStyle = c.color || '#333';
    ctx.arc(c.x, c.y, c.r, 0, Math.PI*2);
    ctx.fill();
    // label
    ctx.fillStyle = "#fff";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";
    ctx.fillText(c.owner || 'player', c.x, c.y+4);
  }
}

// find circle under point
function findCircleAt(x, y){
  for (const [sid, c] of Object.entries(circles)){
    const dx = x - c.x;
    const dy = y - c.y;
    if (Math.sqrt(dx*dx + dy*dy) <= c.r) return {sid, circle: c};
  }
  return null;
}

// get mouse pos
function getPos(e){
  const rect = canvas.getBoundingClientRect();
  const clientX = e.touches ? e.touches[0].clientX : e.clientX;
  const clientY = e.touches ? e.touches[0].clientY : e.clientY;
  return { x: clientX - rect.left, y: clientY - rect.top };
}

// join room
socket.emit('join_room', { room: ROOM_ID });

// events
socket.on('connect', () => {
  console.log('socket connected');
});
socket.on('room_state', (data) => {
  // initial state: circles object keyed by sid
  circles = data.circles || {};
  drawAll();
});
socket.on('circles_update', (data) => {
  circles = data || {};
  drawAll();
});
socket.on('circle_moved', (d) => {
  if (!circles[d.sid]) return;
  circles[d.sid].x = d.x;
  circles[d.sid].y = d.y;
  drawAll();
});
socket.on('player_joined', (d) => {
  document.getElementById('players-count').textContent = 'Players: ' + (d.players.length || 0);
});
socket.on('player_left', (d) => {
  document.getElementById('players-count').textContent = 'Players: ' + (d.players.length || 0);
});
socket.on('error', (e) => console.error('Server error', e));

// leave button
document.getElementById('leave-room').addEventListener('click', () => {
  socket.emit('leave_room', {room: ROOM_ID});
  window.location.href = '/dashboard';
});

// canvas events
canvas.addEventListener('mousedown', (e) => {
  const p = getPos(e);
  const found = findCircleAt(p.x, p.y);
  if (found){
    // only allow dragging own circle (owner==USERNAME)
    if (found.circle.owner !== USERNAME){
      // allow viewing but not dragging others
      return;
    }
    dragging = true;
    dragSid = found.sid;
    offset.x = p.x - found.circle.x;
    offset.y = p.y - found.circle.y;
  }
});

canvas.addEventListener('touchstart', (e) => {
  const p = getPos(e);
  const found = findCircleAt(p.x, p.y);
  if (found && found.circle.owner === USERNAME){
    dragging = true;
    dragSid = found.sid;
    offset.x = p.x - found.circle.x;
    offset.y = p.y - found.circle.y;
  }
}, {passive:false});

window.addEventListener('mousemove', (e) => {
  if (!dragging) return;
  const p = getPos(e);
  const x = p.x - offset.x;
  const y = p.y - offset.y;
  if (circles[dragSid]) {
    circles[dragSid].x = x;
    circles[dragSid].y = y;
    // broadcast to room
    socket.emit('canvas_move', {room: ROOM_ID, x: x, y: y});
    drawAll();
  }
});

window.addEventListener('touchmove', (e) => {
  if (!dragging) return;
  e.preventDefault();
  const p = getPos(e);
  const x = p.x - offset.x;
  const y = p.y - offset.y;
  if (circles[dragSid]) {
    circles[dragSid].x = x;
    circles[dragSid].y = y;
    socket.emit('canvas_move', {room: ROOM_ID, x: x, y: y});
    drawAll();
  }
}, {passive:false});

window.addEventListener('mouseup', () => { dragging = false; dragSid = null; });
window.addEventListener('touchend', () => { dragging = false; dragSid = null; });
