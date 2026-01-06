
import React, { useState } from 'react';

interface InputProps {
  label: string;
  placeholder?: string;
}

const Input: React.FC<InputProps> = ({ label, placeholder }) => {
  const [value, setValue] = useState('');
  return (
    <div className="stencil-input-group">
      <label className="stencil-label">{label}</label>
      <input 
        type="text" 
        className="stencil-input"
        placeholder={placeholder} 
        value={value} 
        onChange={(e) => setValue(e.target.value)} 
      />
    </div>
  );
};

export default Input;
