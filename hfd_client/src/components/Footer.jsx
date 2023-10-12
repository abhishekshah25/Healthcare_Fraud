import React from 'react';
import Typography from '@mui/material/Typography';
import FavoriteIcon from '@mui/icons-material/Favorite';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles((theme) => ({
  footer: {
    backgroundColor: 'black', 
    textAlign: 'center',     
    padding: '16px', 
  },
  textWhite: {
    color: 'white', 
  },
  heartIcon: {
    color: 'red',
    verticalAlign: 'middle',
    fontSize: '1rem', 
  }
}));

const Footer = () => {
  const classes = useStyles();

  return (
    <footer className={classes.footer}>
      <Typography variant="body1" className={classes.textWhite}>
        Designed & Developed with <FavoriteIcon className={classes.heartIcon} /> by Smudgy.
      </Typography>
    </footer>
  );
}

export default Footer;