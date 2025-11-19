// frontend-web/src/components/ReferralModal.jsx
const ReferralModal = ({ transactionId }) => {
  const shareUrl = `https://smartdine.app/invite?ref=${transactionId}`;
  
  const handleShare = () => {
    const text = "¡Pide con SmartDine y gana postres gratis! 🍰";
    window.open(`https://wa.me/?text=${encodeURIComponent(text + " " + shareUrl)}`);
  };

  return (
    <div className="growth-hack-card">
      <h3>🎁 ¡Gana tu próxima comida!</h3>
      <button onClick={handleShare} className="btn-whatsapp">
        Invitar amigos por WhatsApp
      </button>
    </div>
  );
};