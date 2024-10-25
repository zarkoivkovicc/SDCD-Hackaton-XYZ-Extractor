import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';
import logo from './eXYZtract.png';  // Add a logo image in the src folder

function App() {
  const [files, setFiles] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [downloadLinks, setDownloadLinks] = useState([]);
  const [isDownloadingZip, setIsDownloadingZip] = useState(false); // New state for zip download

  const onDrop = (acceptedFiles) => {
    const pdfFiles = acceptedFiles.filter((file) => file.type === 'application/pdf');
    setFiles(pdfFiles);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: 'application/pdf',
    maxFiles: 5,
  });

  const handleProcess = async () => {
    setProcessing(true);
    setDownloadLinks([]);

    try {
      const responses = await Promise.all(
        files.map((file) => {
          const formData = new FormData();
          formData.append('file', file);

          return axios.post('http://localhost:5000/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });
        })
      );

      const allLinks = responses.flatMap((res) => res.data.processed_files);
      setDownloadLinks(allLinks);
    } catch (error) {
      console.error("Error processing files:", error);
    } finally {
      setProcessing(false);
    }
  };

  const handleDownloadZip = async () => {
    setIsDownloadingZip(true); // Start loading animation

    try {
      const response = await axios.get('http://localhost:5000/download_zip', {
        responseType: 'blob', // Important for binary data
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'processed_files.zip'); // Specify the file name
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Error downloading zip:", error);
    } finally {
      setIsDownloadingZip(false); // Stop loading animation
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <img src={logo} alt="App Logo" className="app-logo" />
      </header>
      <div className="description-box">
        <p>Upload your PDF files for processing. Click "Process Files" to start, and download each processed file individually using the provided links.</p>
      </div>

      <div className="upload-container">
        <div {...getRootProps({ className: 'dropzone' })}>
          <input {...getInputProps()} />
          <p>Drag & drop PDF files here, or click to select files</p>
        </div>

        <div className="file-list">
          <h3>Selected Files:</h3>
          {files.map((file, index) => (
            <p key={index}>{file.name}</p>
          ))}
        </div>
      </div>

      <div className="button-container">
        <button onClick={handleProcess} className="process-button" disabled={processing}>
          {processing ? 'Processing...' : 'Process Files'}
        </button>
        <button 
          onClick={handleDownloadZip} 
          className="download-zip-button" 
          disabled={isDownloadingZip} // Disable when downloading
        >
          {isDownloadingZip ? 'Downloading...' : 'Download as Zip'}
        </button>
      </div>

      <div className="download-links">
        <h3>Download Processed Files:</h3>
        {downloadLinks.map((link, index) => (
          <p key={index}>
            <a href={`http://localhost:5000${link.url}`} target="_blank" rel="noopener noreferrer">
              {link.filename}
            </a>
          </p>
        ))}
      </div>
    </div>
  );
}

export default App;