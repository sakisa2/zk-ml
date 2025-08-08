import React, { useState } from 'react';
import type { ChangeEvent, FormEvent } from 'react';
import './App.css';
import "./PredictionPage.css";

const PredictionPage = () => {
  const [formData, setFormData] = useState({
    pol: '',
    starost: '',
    pritisak: '',
    holesterol: '',
  });
  const [showVerify, setShowVerify] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const generateRandomDiagnosis = (): string => {
    let result = '';
    for (let i = 0; i < 10; i++) result += Math.floor(Math.random() * 10);
    return result;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitting(true);
    const payload = { ...formData, salt: generateRandomDiagnosis() };

    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error(`Greška: ${response.status}`);
      const result = await response.json();
      alert('Rezultat sa servera: ' + JSON.stringify(result));

      setFormData({ pol: '', starost: '', pritisak: '', holesterol: '' });
      setShowVerify(true);
    } catch (error) {
      alert('Greška pri slanju podataka: ' + (error as Error).message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleVerify = async () => {
  try {
    const res = await fetch("http://localhost:5000/api/run-script", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ run: true })
    });
    const data = await res.json();
    if (!res.ok || !data.ok) throw new Error(data.stderr || "Greška");
    alert("OK:\n" + (data.stdout || "(nema izlaza)"));
  } catch (e:any) {
    alert("Greška: " + e.message);
  }
};


  return (
    <div className="container">
      <h2>Informacije o pacijentu</h2>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Pol:
          <input
            type="text"
            name="pol"
            placeholder="pol"
            value={formData.pol}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Starost:
          <input
            type="number"
            name="starost"
            placeholder="godine"
            value={formData.starost}
            onChange={handleChange}
            min="0"
            required
          />
        </label>

        <label>
          Pritisak:
          <input
            type="number"
            name="pritisak"
            placeholder="pritisak"
            value={formData.pritisak}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Holesterol:
          <input
            type="number"
            name="holesterol"
            placeholder="količina holesterola"
            value={formData.holesterol}
            onChange={handleChange}
            min="0"
            max="120"
            required
          />
        </label>

        <button type="submit" disabled={submitting}>
          {submitting ? 'Slanje...' : 'Pošalji'}
        </button>

        {showVerify && (
          <button type="button" onClick={handleVerify}>
            Verify
          </button>
        )}
      </form>
    </div>
  );
};

export default PredictionPage;
