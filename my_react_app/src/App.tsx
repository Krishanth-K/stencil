
import React from 'react';
import './index.css'; // Assuming you'll have a main CSS file for global styles
import Button from './components/Button';
import Input from './components/Input';
import Separator from './components/Separator';
import Textbox from './components/Textbox';
import Title from './components/Title';

function App() {
  return (
    <div className="App stencil-container">
      <Title text={'My Awesome App'} />
      <Textbox text={'Welcome to Stencil!\nThis is a simple example of a UI defined in YAML.\n'} />
      <Button label={'Click Me!'} />
      <Separator />
      <Input label={'Your Name'} placeholder={'Enter your name...'} />
      <Button label={'Submit'} />
      <Textbox text={'© 2025 Your Company'} />
    </div>
  );
}

export default App;
