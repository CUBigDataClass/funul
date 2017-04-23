(function() {
  // Initialize Firebase
  const config = {
    apiKey: "AIzaSyBpkRAES6x70xhygiQAg_lN6dv2nlCAw0k",
    authDomain: "funul-8cd90.firebaseapp.com",
    databaseURL: "https://funul-8cd90.firebaseio.com",
    projectId: "funul-8cd90",
    storageBucket: "funul-8cd90.appspot.com",
    messagingSenderId: "1046205384342"
  };
  firebase.initializeApp(config);

  const txtEmail = document.getElementById('txtEmail');
	const txtPassword = document.getElementById('txtPassword');
	const btnLogin = document.getElementById('btnLogin');
	const btnSignUp = document.getElementById('btnSignUp');
	const loginForm = document.getElementById('login_form');
  const btnNavLogin = document.getElementById('navLogin');
  const btnSignOut = document.getElementById('navSignOut');

  //add login event
	btnLogin.addEventListener('click', e => {
		const email = txtEmail.value;
		const pass = txtPassword.value;
		const auth = firebase.auth();
		//sign in
		const promise = auth.signInWithEmailAndPassword(email, pass);
		promise.catch(e => alert(e.message));
    $("#myModal").modal("hide");
	});

	//sign up
	btnSignUp.addEventListener('click', e =>{
		const email = txtEmail.value;
		const pass = txtPassword.value;
		const auth = firebase.auth();
		//sign in
		const promise = auth.createUserWithEmailAndPassword(email, pass);
		promise.catch(e => alert(e.message));
    $("#myModal").modal("hide");
	});

  //sign out
	btnSignOut.addEventListener('click', e => {
		firebase.auth().signOut();
	});

  firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
      // User is signed in.
      var email = user.email;
      var isAnonymous = user.isAnonymous;
      var uid = user.uid;
      btnNavLogin.classList.add('hide');
      btnSignOut.classList.remove('hide');
    } else {
      btnNavLogin.classList.remove('hide');
      btnSignOut.classList.add('hide');
    }
  });

}());
