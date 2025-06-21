function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return decodeURIComponent(parts.pop().split(';').shift());
}

let pausePolling = false;

function placeBid(playerId) {
  pausePolling = true;

  const button = document.querySelector(`[data-player-id="${playerId}"]`);
  if (button) button.textContent = 'Bidding...';

  fetch('/authority/increase-duration/5/')
    .then(res => res.json())
    .catch(err => console.error('Failed to increase duration:', err));

  fetch('/bidding/place-bid/', {
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
    .catch(error => console.error('Error placing bid:', error))
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


// ----------------------------
// Auction control buttons (new)
// ----------------------------

document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('start-auction-btn');
  const pauseBtn = document.getElementById('pause-auction-btn');
  const endBtn = document.getElementById('end-auction-btn');

  if (startBtn) {
    startBtn.addEventListener('click', () => {
      fetch('/authority/start-auction/')
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            console.log('Auction started');
            startBtn.disabled = true;
            pauseBtn.disabled = false;
            endBtn.disabled = false;
          } else {
            alert(data.error || 'Failed to start auction');
          }
        });
    });
  }

  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      fetch('/authority/pause-auction/')
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            console.log('Auction paused');
            pauseBtn.textContent = 'Resume Auction';
            pauseBtn.id = 'resume-auction-btn';
          }
        });
    });
  }

  if (endBtn) {
    endBtn.addEventListener('click', () => {
      fetch('/authority/end-auction/')
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            console.log('Auction ended');
            startBtn.disabled = false;
            pauseBtn.disabled = true;
            endBtn.disabled = true;
          }
        });
    });
  }
});
