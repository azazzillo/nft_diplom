console.log('hello');
async function registerWithMetaMask() {
    if (window.ethereum) {
        window.web3 = new Web3(ethereum);
        console.log('hello');
        try {
            console.log('hello');
            // Request account access if needed
            await ethereum.enable();
            // Accounts now exposed
            const accounts = await web3.eth.getAccounts();
            const walletAddress = accounts[0];
            // Send the wallet address to the server to create/register the user
            createUserOnServer(walletAddress);
            console.log(accounts[0]);
            console.log(walletAddress);
        } catch (error) {
            // User denied account access
            console.error('User denied account access');
        }
    } else if (window.web3) {
        console.log('hello');
        window.web3 = new Web3(web3.currentProvider);
        // Accounts always exposed
        const accounts = await web3.eth.getAccounts();
        const walletAddress = accounts[0];
        // Send the wallet address to the server to create/register the user
        createUserOnServer(walletAddress);
    } else {
        console.log('Non-Ethereum browser detected. You should consider trying MetaMask!');
    }
}

async function createUserOnServer(walletAddress) {
    try {
        const response = await fetch('to_login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(), // Get CSRF token if using Django
            },
            body: JSON.stringify({ wallet_address: walletAddress }),
        });

        if (response.ok) {
            console.log('User created successfully!');
            // Redirect to the desired page
            window.location.href = '/reg/to_login/';
        } else {
            console.error('Failed to create user');
        }
    } catch (error) {
        console.error('Error creating user:', error);
    }
}


function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.split('=');
        if (name.trim() === 'csrftoken') {
            return value;
        }
    }
    return '';
}