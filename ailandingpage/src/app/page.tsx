import React from 'react';
import Home from '../pages/home';
import './page.css';
export default function Page() {
  return (
    <div className='homepage'>
      <div className='background-images'>
        <img className='background-image-audi' src={'/assets/images/bk/A3.png'} alt='AudiBackground' />
        <div className='separator'/>
        <img className='background-image-code' src={'/assets/images/bk/Code.jpg'} alt='CodeBackground' />
      </div>
      <Home />
      <div className='footer'>
        <img className='footer-logo' src={'/assets/icons/github-mark-white.svg'} alt='Logo' />
        <img className='footer-logo' src={'/assets/icons/iconmonstr-linkedin-3.svg'} alt='Logo' />
      </div>
    </div>
  );
}
