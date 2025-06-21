function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
}

let pausePolling = false;

function placeBid(playerId) {
  pausePolling = true;
  console.log('Placing bid for player:', playerId);

  const button = document.querySelector(`[data-player-id="${playerId}"]`);
  if (button) button.textContent = 'Bidding...';

  fetch('/authority/increase-duration/5/')
    .then(res => res.json())
    .then(data => {
      console.log('Duration increased:', data);
    })
    .catch(err => console.error('Failed to increase duration:', err));

  fetch('place-bid/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ player_id: playerId }),
  })
    .then(res => res.json())
    .then(data => {
      if (!data.success) alert(data.message || 'Bid failed');
    })
    .catch(error => {
      console.error('Error placing bid:', error);
    })
    .finally(() => {
      if (button) button.textContent = 'Place bid';
      setTimeout(() => {
        pausePolling = false;
      }, 1000);
    });
}

function attachBidButtonListener() {
  const btn = document.querySelector('.place-bid-btn');
  if (btn) {
    btn.addEventListener('click', () => {
      const playerId = btn.getAttribute('data-player-id');
      placeBid(playerId);
    });
  }
}

// Poll every 500ms unless paused
setInterval(() => {
  if (!pausePolling) updateAuctionInfo();
}, 500);
