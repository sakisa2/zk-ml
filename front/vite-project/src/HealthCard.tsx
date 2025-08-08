import React from 'react';
import './HealthCard.css';

interface HealthCardProps {
  image: string;
  description: string;
  onPredict: () => void;
}

const HealthCard: React.FC<HealthCardProps> = ({ image, description, onPredict }) => {
  return (
    <div className="health-card">
      <img src={image} alt="Health" className="card-image" />
      <p className="card-description">{description}</p>
      <button className="card-button" onClick={onPredict}>
        Predict Your Disease
      </button>
    </div>
  );
};

export default HealthCard;
