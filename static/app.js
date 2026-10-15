/* static/app.js */
const gridW = 4, gridH = 5;
const canvas = document.getElementById('board-canvas');
const ctx = canvas.getContext('2d');
const video = document.getElementById('video');
let showGrid = true;
let backgroundImg = null;
let pieces = [];
let addMode = false;
let removeMode = false;
let lastSolution = null;

const startCameraBtn = document.getElementById('start-camera');
const captureBtn = document.getElementById('capture');
const uploadInput = document.getElementById('image-upload');
const detectBtn = document.getElementById('detect');
const toggleGridBtn = document.getElementById('toggle-grid');
const fitBackgroundBtn = document.getElementById('fit-background');
const clearPiecesBtn = document.getElementById('clear-pieces');
const addPieceModeBtn = document.getElementById('add-piece-mode');
const removePieceModeBtn = document.getElementById('remove-piece-mode');
const pieceWSelect = document.getElementById('piece-w');
const pieceHSelect = document.getElementById('piece-h');
const pieceColorInput = document.getElementById('piece-color');
const presetsDiv = document.getElementById('presets');
const solveBtn = document.getElementById('solve');
const animateBtn = document.getElementById('animate');
const keyPieceInput = document.getElementById('key-piece');
const goalXInput = document.getElementById('goal-x');
const goalYInput = document.getElementById('goal-y');
const statusDiv = document.getElementById('status');

const cellW = canvas.width / gridW;
const cellH = canvas.height / gridH;

async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    video.style.display = 'block';
  } catch (e) {
    alert('Camera error: ' + e.message);
  }
}
startCameraBtn.onclick = startCamera;

captureBtn.onclick = () => {
  const tmp = document.createElement('canvas');
  tmp.width = canvas.width; tmp.height = canvas.height;
  const tctx = tmp.getContext('2d');
  tctx.drawImage(video, 0, 0, tmp.width, tmp.height);
  backgroundImg = new Image();
  backgroundImg.src = tmp.toDataURL();
  backgroundImg.onload = draw;
};

uploadInput.onchange = (e) => {
  const f = e.target.files[0];
  if (!f) return;
  const url = URL.createObjectURL(f);
  backgroundImg = new Image();
  backgroundImg.onload = () => { draw(); URL.revokeObjectURL(url); };
  backgroundImg.src = url;
};

detectBtn.onclick = async () => {
  if (!backgroundImg) { alert('Capture or upload an image first'); return; }
  statusDiv.textContent = 'Uploading image for detection...';
  const blob = await (await fetch(backgroundImg.src)).blob();
  const fd = new FormData();
  fd.append('image', blob, 'capture.png');
  const resp = await fetch('/api/detect', {method: 'POST', body: fd});
  if (!resp.ok) { const txt = await resp.text(); statusDiv.textContent = 'Detect failed: '+txt; return; }
  const data = await resp.json();
  pieces = data.pieces.map((p,i)=>({x:p.x,y:p.y,w:p.w,h:p.h,color: i===3? '#ff6666': randomPastel(i)}));
  statusDiv.textContent = `Detected ${pieces.length} pieces`;
  draw();
};

canvas.addEventListener('click', (ev) => {
  const rect = canvas.getBoundingClientRect();
  const cx = ev.clientX - rect.left;
  const cy = ev.clientY - rect.top;
  const gx = Math.floor(cx / cellW);
  const gy = Math.floor(cy / cellH);
  if (addMode) {
    const w = parseInt(pieceWSelect.value, 10);
    const h = parseInt(pieceHSelect.value, 10);
    if (canPlaceAt(gx, gy, w, h, -1)) {
      pieces.push({x: gx, y: gy, w, h, color: pieceColorInput.value}); draw();
    } else alert('Cannot place piece here');
  } else if (removeMode) {
    for (let i=0;i<pieces.length;i++){
      const p = pieces[i];
      if (gx>=p.x && gx<p.x+p.w && gy>=p.y && gy<p.y+p.h) { pieces.splice(i,1); draw(); return; }
    }
  }
});

function canPlaceAt(x,y,w,h,indexToIgnore){
  if (x<0||y<0||x+w>gridW||y+h>gridH) return false;
  for (let i=0;i<pieces.length;i++){ if (i===indexToIgnore) continue; const p=pieces[i]; if (!(x+w<=p.x||p.x+p.w<=x||y+h<=p.y||p.y+p.h<=y)) return false; }
  return true;
}

function draw(statePieces=null, highlightIdx=-1){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  if (backgroundImg) ctx.drawImage(backgroundImg,0,0,canvas.width,canvas.height);
  if (showGrid) drawGrid();
  const arr = statePieces||pieces;
  for (let i=0;i<arr.length;i++){
    const p = arr[i]; const x=p.x*cellW; const y=p.y*cellH; const w=p.w*cellW; const h=p.h*cellH;
    ctx.fillStyle = p.color||'#EAD2A2'; ctx.globalAlpha=0.95; ctx.fillRect(x+4,y+4,w-8,h-8); ctx.globalAlpha=1;
    ctx.strokeStyle=(i===highlightIdx)?'#ff4b4b':'#222'; ctx.lineWidth=3; ctx.strokeRect(x+4,y+4,w-8,h-8);
    ctx.fillStyle='#111'; ctx.font='20px sans-serif'; ctx.fillText(String(i), x+8, y+26);
  }
}
function drawGrid(){ ctx.strokeStyle='rgba(255,255,255,0.15)'; ctx.lineWidth=1; for(let i=0;i<=gridW;i++){ const x=i*cellW; ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); } for(let j=0;j<=gridH;j++){ const y=j*cellH; ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); } }

function randomPastel(i){ const hue = (i*47)%360; return `hsl(${hue} 70% 75%)`; }

presetsDiv.addEventListener('click',(ev)=>{ const btn = ev.target.closest('button'); if(!btn) return; const lvl = parseInt(btn.dataset.level,10); loadPreset(lvl); });
function loadPreset(n){ const ps = {
 1: {sizes:[[1,1,1,1,2,1,2,1,1,1],[2,2,2,2,1,1,2,1,1,1]], positions:[[1,2,0,3,1,0,1,3,0,3],[0,0,1,1,2,3,3,3,4,4]]},
 2: {sizes:[[1,1,2,1,1,2,2,1,1,1,2,1],[1,1,1,1,1,1,1,1,1,1,2,1]], positions:[[0,1,2,0,1,2,0,2,3,0,1,3],[0,0,0,1,1,1,2,2,2,3,3,3]]},
 3: {sizes:[[2,1,1,1,1,1,1,2,1,1],[1,2,1,2,2,1,2,2,1,1]], positions:[[2,0,1,2,3,1,0,1,3,3],[0,1,1,1,1,2,3,3,3,4]]},
 4: {sizes:[[1,1,1,1,1,1,2,1,2,1],[2,1,1,2,1,1,1,2,2,2]], positions:[[0,1,2,3,1,2,1,0,1,3],[0,0,0,0,1,1,2,3,3,3]]}
 }[n]; if(!ps) return; pieces=[]; const sx=ps.sizes[0], sy=ps.sizes[1], px=ps.positions[0], py=ps.positions[1]; for(let i=0;i<px.length;i++){ pieces.push({x:px[i], y:py[i], w:sx[i], h:sy[i], color: i===3? '#ff6666': randomPastel(i)}); } draw(); }

solveBtn.onclick = async ()=>{
  if (pieces.length===0){ statusDiv.textContent='No pieces placed'; return; }
  const payload = { pieces: pieces.map(p=>({x:p.x,y:p.y,w:p.w,h:p.h})), key_index: parseInt(keyPieceInput.value||'3',10), goal:{x:parseInt(goalXInput.value||'0',10), y:parseInt(goalYInput.value||'0',10)} };
  statusDiv.textContent='Solving on server...';
  const resp = await fetch('/api/solve', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
  if(!resp.ok){ const txt = await resp.text(); statusDiv.textContent='Solve failed: '+txt; return; }
  const data = await resp.json(); if(!data.path){ statusDiv.textContent='No path returned'; return; }
  lastSolution = data.path; statusDiv.textContent = `Solved in ${data.moves} moves (visited ${data.visited})`;
};

animateBtn.onclick = async ()=>{
  if(!lastSolution){ statusDiv.textContent='No solution available. Press Solve first.'; return; }
  for(let i=0;i<lastSolution.length;i++){ const s = lastSolution[i]; const statePieces = s.xs.map((vx, idx)=>{ const base = pieces[idx] || {w:1,h:1,color: randomPastel(idx)}; return {x: s.xs[idx], y: s.ys[idx], w: base.w, h: base.h, color: pieces[idx]? pieces[idx].color : randomPastel(idx)} }); draw(statePieces); statusDiv.textContent = `Step ${i}/${lastSolution.length-1}`; await new Promise(r=>setTimeout(r,550)); } statusDiv.textContent='Animation finished.'; }

// initial draw
draw();
