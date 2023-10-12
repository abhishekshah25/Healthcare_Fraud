import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles((theme) => ({
  title: {
    flexGrow: 1, 
    textAlign: 'center',
  },
}));

function Navbar() {
  const classes = useStyles();

  return (
    <AppBar style={{ backgroundColor: 'black' }} position="static">
      <Toolbar>
        <Typography variant="h5" className={classes.title}>
          Healthcare Fraud Detection
        </Typography>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;