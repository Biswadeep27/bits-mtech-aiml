import React from 'react';
import TextCorrection from './TextCorrection';
import FileCorrection from './FileCorrection';
import { Container, Typography, Box } from '@mui/material';
import './styles.css';

function App() {
  return (
    <Container maxWidth="lg">
      <Box sx={{ textAlign: 'center', mt: 5 }}>
        <Typography variant="h3" gutterBottom>
          Spelling Correction App
        </Typography>
        <TextCorrection />
        <FileCorrection />
      </Box>
    </Container>
  );
}

export default App;
