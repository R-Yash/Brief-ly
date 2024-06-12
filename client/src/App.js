import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Card from './Card';
import Header from './Header';
import Footer from './Footer';
import './App.css';

const App = () => {
    const [jsonFiles, setJsonFiles] = useState([]);
    const [isDarkMode, setIsDarkMode] = useState(false);

    useEffect(() => {
        axios.get('https://brief-ly.onrender.com/news')
            .then(response => {
                const filteredData = response.data.filter(file => file.content.trim() !== "");
                setJsonFiles(filteredData);
            })
            .catch(error => {
                console.error('There was an error fetching the data!', error);
            });
    }, []);

    useEffect(() => {
        document.body.classList.toggle('dark-mode', isDarkMode);
    }, [isDarkMode]);

    const toggleDarkMode = () => {
        setIsDarkMode(prevMode => !prevMode);
    };

    return (
        <div className="app">
            <Header toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode} />
            <main>
                <div className="card-container">
                    {jsonFiles.map(file => (
                        <Card
                            key={file.id}
                            title={file.title}
                            content={file.content}
                            image={file.image}
                            link={file.link}
                        />
                    ))}
                </div>
            </main>
            <Footer />
        </div>
    );
}

export default App;
