import React, { useState } from 'react';

interface ClientFormData {
  lastName: string;
  firstName: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  zipCode: string;
}

const initialFormData: ClientFormData = {
  lastName: '',
  firstName: '',
  email: '',
  phone: '',
  address: '',
  city: '',
  zipCode: ''
};

export const CreateClientForm: React.FC = () => {
  const [formData, setFormData] = useState<ClientFormData>(initialFormData);
  const [status, setStatus] = useState<{ type: 'success' | 'error' | ''; message: string }>({ type: '', message: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setStatus({ type: '', message: '' });

    // Basic validation
    if (!formData.lastName || !formData.firstName || !formData.phone) {
      setStatus({ type: 'error', message: 'Veuillez remplir les champs obligatoires (Nom, Prénom, Téléphone).' });
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await fetch('/api/clients/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la création du client');
      }

      // Success
      const data = await response.json();
      console.log('Client created:', data);
      setStatus({ type: 'success', message: 'Client créé avec succès !' });
      setFormData(initialFormData); // Reset form
    } catch (error) {
      console.error('Error:', error);
      setStatus({ type: 'error', message: "Impossible de créer le client. Vérifiez que le backend est lancé." });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="client-form-container">
      <h2>Nouveau Client</h2>
      
      {status.message && (
        <div className={`status-message ${status.type}`}>
          {status.message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="client-form">
        <div className="form-group">
          <label htmlFor="lastName">Nom *</label>
          <input
            type="text"
            id="lastName"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
            placeholder="Dupont"
          />
        </div>

        <div className="form-group">
          <label htmlFor="firstName">Prénom *</label>
          <input
            type="text"
            id="firstName"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
            placeholder="Jean"
          />
        </div>

        <div className="form-group">
          <label htmlFor="phone">Téléphone *</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            required
            placeholder="06 12 34 56 78"
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="jean.dupont@email.com"
          />
        </div>

        <div className="form-group">
          <label htmlFor="address">Adresse</label>
          <input
            type="text"
            id="address"
            name="address"
            value={formData.address}
            onChange={handleChange}
            placeholder="123 Rue de la République"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="zipCode">Code Postal</label>
            <input
              type="text"
              id="zipCode"
              name="zipCode"
              value={formData.zipCode}
              onChange={handleChange}
              placeholder="75001"
              maxLength={5}
            />
          </div>

          <div className="form-group">
            <label htmlFor="city">Ville</label>
            <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleChange}
              placeholder="Paris"
            />
          </div>
        </div>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Envoi...' : 'Créer le Client'}
        </button>
      </form>
    </div>
  );
};
