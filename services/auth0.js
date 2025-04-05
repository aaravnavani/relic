// auth0.js
import Auth0 from 'react-native-auth0';

const auth0 = new Auth0({
  domain: 'dev-x6ilpefvd66wtu4x.us.auth0.com',
  clientId: 'YOUR_AUTH0_CLIENT_ID'
});

export default auth0;
