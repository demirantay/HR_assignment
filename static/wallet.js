window.rentverseWallet = { address: null };

(function () {
  const btn = document.getElementById("wallet-connect-btn");
  const statusEl = document.getElementById("wallet-status");

  function short(addr) { return addr ? `${addr.slice(0, 6)}...${addr.slice(-4)}` : ""; }

  async function connectWallet() {
    if (!window.ethereum) {
      alert("No wallet found. Install MetaMask and reload the page.");
      return;
    }
    try {
      btn.disabled = true;
      btn.textContent = "Connecting...";
      const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
      window.rentverseWallet.address = accounts[0];
      btn.textContent = short(accounts[0]);
      statusEl.textContent = "Connected";
      statusEl.classList.add("connected");
    } catch (err) {
      console.error(err);
      btn.textContent = "Connect Wallet";
    } finally {
      btn.disabled = false;
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    if (btn) btn.addEventListener("click", connectWallet);
    if (window.ethereum) {
      window.ethereum.request({ method: "eth_accounts" }).then((accounts) => {
        if (accounts.length > 0) {
          window.rentverseWallet.address = accounts[0];
          btn.textContent = short(accounts[0]);
          statusEl.textContent = "Connected";
          statusEl.classList.add("connected");
        }
      });
      window.ethereum.on("accountsChanged", () => window.location.reload());
    }
  });
})();