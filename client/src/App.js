import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Card from './Card';
import Header from './Header';
import Footer from './Footer';
import './App.css';

const App = () => {
    const [jsonFiles, setJsonFiles] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:5000/news')
            .then(response => {
                const filteredData = response.data.filter(file => file.content.trim() !== "");
                setJsonFiles(filteredData);
            })
            .catch(error => {
                console.error('There was an error fetching the data!', error);
            });
    }, []);

    return (
        <div className="app">
            <Header />
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
