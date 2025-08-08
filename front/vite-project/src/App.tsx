import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import HealthCard from './HealthCard';
import PredictionPage from './PredictionPage';

import cardioImage from './assets/cardiovascular_system_1000x667.jpg';

function App() {
  const navigate = useNavigate();

  const handlePredict = () => {
    // Preusmeri na novu stranicu
    navigate('/prediction');
  };

  return (
    <Routes>
      <Route path="/" element={
        <div className="App">
          <h1>Disease Predictor</h1>
          <HealthCard
            image={cardioImage}
            description="Our app helps predict the risk of heart disease based on personal health information such as age, blood pressure, cholesterol levels, and more. By analyzing this data with machine learning, we provide early insights to support preventive care and healthier lives."
            onPredict={handlePredict}
          />
        </div>
      } />
      <Route path="/prediction" element={<PredictionPage />} />
    </Routes>
  );
}

export default App;
