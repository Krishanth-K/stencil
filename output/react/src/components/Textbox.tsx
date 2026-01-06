
import React from 'react';

interface TextboxProps {
  text: string;
}

const Textbox: React.FC<TextboxProps> = ({ text }) => {
  return <p className="stencil-text">{text}</p>;
};

export default Textbox;
