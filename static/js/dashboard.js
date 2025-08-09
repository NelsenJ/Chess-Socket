// Simple ajax to create room and refresh list
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('create-room-btn');
  const input = document.getElementById('room-name');
  const list = document.getElementById('rooms-list');

  btn.addEventListener('click', async () => {
    const name = input.value.trim();
    if (!name) return alert("Masukkan nama room");
    try {
      const res = await fetch('/api/create_room', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name})
      });
      const data = await res.json();
      if (data.ok) {
        window.location.href = `/room/${data.room_id}`;
      } else {
        alert('Gagal buat room: ' + (data.error || 'unknown'));
      }
    } catch (e) {
      alert('Error: ' + e.message);
    }
  });

  // Optionally: refresh list every 5s
  async function refreshRooms(){
    try {
      const r = await fetch('/api/list_rooms');
      const j = await r.json();
      if (j.ok){
        list.innerHTML = '';
        j.rooms.forEach(rm => {
          const li = document.createElement('li');
          li.innerHTML = `<strong>${rm.name}</strong> (${rm.players} players)
            <a class="join-link" href="/room/${rm.id}">Join</a>`;
          list.appendChild(li);
        });
      }
    } catch(e){}
  }
  setInterval(refreshRooms, 5000);
});
