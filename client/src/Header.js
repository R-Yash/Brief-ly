import React from 'react';
import './Header.css';

const Header = ({ toggleDarkMode, isDarkMode }) => {
    return (
        <header className="header">
            <h1 className="header-title">Briefly</h1>
            <div className="header-icons">
                <a href="https://github.com/your-repo-link" target="_blank" rel="noopener noreferrer">
                    <img src="https://img.icons8.com/material-outlined/24/000000/github.png" alt="GitHub" className="icon" />
                </a>
                <button className="icon-button" onClick={toggleDarkMode}>
                    <img 
                        src={isDarkMode ? "https://img.icons8.com/ios-glyphs/30/ffffff/sun--v1.png" : "https://img.icons8.com/ios-glyphs/30/000000/moon-symbol.png"} 
                        alt="Dark Mode Toggle" 
                        className="icon" 
                    />
                </button>
            </div>
        </header>
    );
}

export default Header;
