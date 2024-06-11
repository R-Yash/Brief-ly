import React from 'react';
import './Card.css'; // Import the CSS file for styling

const Card = ({ title, content, image, link }) => {
    return (
        <div className="card">
            <img src={image} alt={title} className="card-image" />
            <h3 className="card-title">{title}</h3>
            <p className="card-content">{content}</p>
            <a href={link} className="card-link" target="_blank" rel="noopener noreferrer">
                <img src="https://img.icons8.com/material-outlined/24/000000/link.png" alt="link icon" />
            </a>
        </div>
    );
}

export default Card;
