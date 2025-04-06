// components/LoginButton.tsx
import React from 'react';
import { StyleSheet, View, Button, Text } from 'react-native';
import { useAuth0 } from 'react-native-auth0';

const LoginButton: React.FC = () => {
  const { authorize, user } = useAuth0();

  const handleLogin = async () => {
    try {
      // Initiate the Auth0 login flow
      await authorize();
      // {
      //   // scope: 'openid profile email',
      //   redirectUrl: 'com.anonymous.relic.myapp://dev-x6ilpefvd66wtu4x.us.auth0.com/ios/com.anonymous.relic/callback'
      //   redirectUrl: "myapp://callback"
      // }
      console.log('Logged in successfully!');
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <View style={styles.container}>
      {!user ? (  
        <Button title="Log In" onPress={handleLogin} />
      ) : (
        <Text style={styles.welcome}>
          Welcome, {user.name || user.email}!
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginVertical: 20,
  },
  welcome: {
    fontSize: 18,
    marginVertical: 10,
  },
});

export default LoginButton;
