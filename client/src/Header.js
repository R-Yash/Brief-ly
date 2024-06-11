import React from 'react';
import './Header.css';

const Header = () => {
    return (
        <header className="header">
            <h1 className="header-title">Briefly</h1>
            <div className="header-icons">
                <a href="https://github.com/R-Yash/briefly" target="_blank" rel="noopener noreferrer">
                    <img src="https://img.icons8.com/material-outlined/24/000000/github.png" alt="GitHub" className="icon" />
                </a>
                <button className="icon-button" onClick={() => alert('Toggle Dark Mode')}>
                    <img src="https://img.icons8.com/material-outlined/24/000000/moon-symbol.png" alt="Dark Mode Toggle" className="icon" />
                </button>
            </div>
        </header>
    );
}

export default Header;
