import React, {useState} from 'react';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';
import { tableCellClasses } from '@mui/material/TableCell';


const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

const MainContent = () => {

  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [uploadSuccess, setUploadSuccess] = useState(false); 
  const [predictionData, setPredictionData] = useState(null);

  const buttonStyle = {
    backgroundColor: 'yellow',
    color: 'black',
    borderRadius: '16px', 
  };

  const predictButtonStyle = {
    backgroundColor: 'green', 
    color: 'white', 
    borderRadius: '16px',
    padding: '8px 16px',
  };

  const paperStyle = {
    padding: '8px',
    border: '1px solid #ccc', 
    borderRadius: '16px',
    maxWidth: '300px',
    margin: '0 auto', 
  };

  const textStyle = {
    fontSize: '20px', 
    fontWeight: 'bold', 
    color: '#333', 
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFiles([...uploadedFiles, file]);
      setUploadSuccess(true);
    }
  };
  
  const handlePredict = async () => {

    try {
      if (uploadedFiles.length < 4) {
        console.error('Kindly upload all necessary files');
        return;
      }

      const formData = new FormData();

      for(let i = 0; i < uploadedFiles.length; i++){
        formData.append('uploadedFiles',uploadedFiles[i]);
      }

      const response = await fetch('http://127.0.0.1:5000/api/predict', {
        method: 'POST',
        body: formData,
        headers: {
          'Access-Control-Allow-Origin': '*', 
        },
      })
      const data = await response.json(); 

      setPredictionData(data);

      console.log('Prediction results:', data);

    } catch (error) {
        console.error('Prediction error:', error);
      }
  };
  
  const filers = ['Provider IDs', 'Beneficiary Data', 'Inpatient Data', 'Outpatient Data'];

  return (
    <>
    {filers.map((filer, index) => (
    <Grid container spacing={2} alignItems="center" justifyContent="center">
          <React.Fragment key={index}>
            <Grid item xs={12} sm={4} style={{ marginBottom: '10px' }}>
              <Paper style={paperStyle}>
                <Typography variant="h5" align="center" style={textStyle}>
                  {filer}
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={3} align="center">
              <Button
                variant="contained"
                component="label"
                color="primary"
                style={buttonStyle}
              >
                <input type="file" onChange={handleFileUpload} />
              </Button>
            </Grid>
          </React.Fragment>
      </Grid> 
      ))};

    <div style={{ marginBottom: '20px' }}></div>

    <Grid container spacing={2} alignItems="center" justifyContent="center">
      <Grid item xs={12} sm={4} align="center">
        <Button
          variant="contained"
          color="primary"
          style={predictButtonStyle}
          size = "medium"
          onClick={handlePredict}
        >
          Predict Result
        </Button>
      </Grid> 
    </Grid>

    <div style={{ marginBottom: '20px' }}></div>

    {predictionData && (
        <Grid container spacing={2} alignItems="center" justifyContent="center">
          <Grid item xs={12} sm={12}>
            <Paper sx={{ width: '80%', margin: '20px auto' }}>
              <TableContainer >
              <Table sx={{ minWidth: 500 }} aria-label="customized table">
                <TableHead>
                  <StyledTableRow>
                  <StyledTableCell>Observations</StyledTableCell>
                  <StyledTableCell>Quantum</StyledTableCell>
                  </StyledTableRow>
                </TableHead>
                <TableBody>
                  <StyledTableRow>
                  <StyledTableCell>Total Count of Claims</StyledTableCell>
                  <StyledTableCell>{predictionData.total_cnt}</StyledTableCell>
                  </StyledTableRow>
                  <StyledTableRow>
                    <StyledTableCell>Count of Fraud Claims</StyledTableCell>
                    <StyledTableCell>{predictionData.fraud_cnt}</StyledTableCell>
                  </StyledTableRow>
                  <StyledTableRow>
                  <StyledTableCell>Count of Non-Fraud Claims</StyledTableCell>
                    <StyledTableCell>{predictionData.non_fraud_cnt}</StyledTableCell>
                  </StyledTableRow>
                  <StyledTableRow>
                  <StyledTableCell>Fraud Percentage</StyledTableCell>
                  <StyledTableCell>{predictionData.fraud_prcnt}%</StyledTableCell>
                  </StyledTableRow>
                </TableBody>
              </Table>
            </TableContainer>
            </Paper>
          </Grid>
        </Grid>
      )}
    </>
  );
}

export default MainContent;
