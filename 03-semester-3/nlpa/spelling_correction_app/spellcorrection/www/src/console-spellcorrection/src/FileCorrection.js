import React, { useState } from 'react';
import { BaseUrl } from './appConfig';
import { Button, Typography, Box, Paper, Container, CircularProgress } from '@mui/material';

function FileCorrection() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [downloadLink, setDownloadLink] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setDownloadLink(''); // Clear the previous download link when a new file is selected
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true); // Set loading to true when the API call starts

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`${BaseUrl}/correct_file`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      const fileName = Object.keys(data)[0];
      setDownloadLink(data[fileName]);
    } catch (error) {
      console.error('Error correcting file:', error);
    } finally {
      setLoading(false); // Set loading to false when the API call ends
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 5 }}>
      <Typography variant="h4" gutterBottom>
        File Correction
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Button
          variant="contained"
          component="label"
          sx={{ mb: 3 }}
        >
          Upload File
          <input
            type="file"
            hidden
            onChange={handleFileChange}
          />
        </Button>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={!selectedFile || loading} // Disable button during loading
        >
          {loading ? 'Processing...' : 'Upload and Correct File'}
        </Button>
      </Box>
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <CircularProgress />
        </Box>
      )}
      {downloadLink && (
        <Paper elevation={3} sx={{ mt: 3, p: 2, textAlign: 'center' }}>
          <Typography variant="h6">Download Corrected File</Typography>
          <Button variant="contained" color="secondary" href={downloadLink} download>
            Download
          </Button>
        </Paper>
      )}
    </Container>
  );
}

export default FileCorrection;
