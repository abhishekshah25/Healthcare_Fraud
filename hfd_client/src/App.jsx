import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import MainContent from './components/MainContent';
import backgroundImage from './assets/healthy.jpg';
import './App.css';

const backgroundStyle = {
  backgroundImage: `url(${backgroundImage})`,
  backgroundSize: '100% 95%',
  backgroundRepeat: 'no-repeat',
  backgroundAttachment: 'fixed', 
};

const App = () => {

  return (
    <div className = "app-container" style = {backgroundStyle}>
      <Navbar />
      <div className="main-content">
        <MainContent />
      </div>
      <div>
        <Footer className="footer"/>
      </div>
    </div> 
  )
}

export default App;
