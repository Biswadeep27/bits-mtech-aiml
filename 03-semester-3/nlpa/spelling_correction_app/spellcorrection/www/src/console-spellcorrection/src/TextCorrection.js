import React, { useState } from 'react';
import debounce from 'lodash.debounce';
import { BaseUrl } from './appConfig';
import { TextField, Box, Typography, Paper, Container } from '@mui/material';

function TextCorrection() {
  const [inputText, setInputText] = useState('');
  const [correctedText, setCorrectedText] = useState('');

  const fetchCorrectedText = async (text) => {
    try {
      const response = await fetch(`${BaseUrl}/correct`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setCorrectedText(data.corrected_text);
    } catch (error) {
      console.error('Error correcting text:', error);
    }
  };

  const debouncedFetchCorrectedText = debounce(fetchCorrectedText, 300);

  const handleTextChange = (event) => {
    const text = event.target.value;
    setInputText(text);

    if (text.trim() === '') {
      setCorrectedText('');
    } else {
      debouncedFetchCorrectedText(text);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 5 }}>
      <Typography variant="h4" gutterBottom>
        Text Correction
      </Typography>
      <TextField
        label="Enter text with spelling mistakes"
        variant="outlined"
        fullWidth
        multiline
        rows={10}
        value={inputText}
        onChange={handleTextChange}
        sx={{ mb: 3 }}
      />
      <Paper elevation={3} sx={{ p: 2 }}>
        <Typography variant="h6">Corrected Text</Typography>
        <Box sx={{ whiteSpace: 'pre-wrap', mt: 1 }}>
          {correctedText || 'Corrected text will appear here...'}
        </Box>
      </Paper>
    </Container>
  );
}

export default TextCorrection;

