// Frontend Integration Tests for Farm Produce Marketplace
// Run with: node test_frontend.js

const axios = require('axios');

const BASE_URL = 'http://localhost:5000';
let farmerToken = '';
let buyerToken = '';
let productId = '';

// Test utilities
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

const testAPI = async (method, endpoint, data = null, token = null) => {
    try {
        const config = {
            method,
            url: `${BASE_URL}${endpoint}`,
            headers: token ? { 'Authorization': `Bearer ${token}` } : {},
        };
        
        if (data) {
            config.data = data;
            config.headers['Content-Type'] = 'application/json';
        }
        
        const response = await axios(config);
        return { success: true, data: response.data, status: response.status };
    } catch (error) {
        return { 
            success: false, 
            error: error.response?.data?.message || error.message,
            status: error.response?.status 
        };
    }
};

// Test cases
const tests = {
    async testServerConnection() {
        console.log('🔍 Testing server connection...');
        const result = await testAPI('GET', '/');
        if (result.success) {
            console.log('✅ Server is running');
            return true;
        } else {
            console.log('❌ Server connection failed:', result.error);
            return false;
        }
    },

    async testUserRegistration() {
        console.log('🔍 Testing user registration...');
        
        // Test farmer registration
        const farmerData = {
            name: 'Test Farmer',
            email: 'testfarmer@example.com',
            password: 'password123',
            role: 'farmer'
        };
        
        const farmerResult = await testAPI('POST', '/register', farmerData);
        if (farmerResult.success) {
            farmerToken = farmerResult.data.token;
            console.log('✅ Farmer registration successful');
        } else {
            console.log('❌ Farmer registration failed:', farmerResult.error);
            return false;
        }
        
        // Test buyer registration
        const buyerData = {
            name: 'Test Buyer',
            email: 'testbuyer@example.com',
            password: 'password123',
            role: 'buyer'
        };
        
        const buyerResult = await testAPI('POST', '/register', buyerData);
        if (buyerResult.success) {
            buyerToken = buyerResult.data.token;
            console.log('✅ Buyer registration successful');
            return true;
        } else {
            console.log('❌ Buyer registration failed:', buyerResult.error);
            return false;
        }
    },

    async testUserLogin() {
        console.log('🔍 Testing user login...');
        
        const loginData = {
            email: 'testfarmer@example.com',
            password: 'password123'
        };
        
        const result = await testAPI('POST', '/login', loginData);
        if (result.success && result.data.token) {
            console.log('✅ Login successful');
            return true;
        } else {
            console.log('❌ Login failed:', result.error);
            return false;
        }
    },

    async testProductManagement() {
        console.log('🔍 Testing product management...');
        
        // Create product
        const productData = {
            name: 'Fresh Tomatoes',
            price: 5.99,
            category: 'Vegetables',
            stock: 100,
            description: 'Fresh organic tomatoes from our farm'
        };
        
        const createResult = await testAPI('POST', '/products', productData, farmerToken);
        if (createResult.success) {
            productId = createResult.data.id;
            console.log('✅ Product creation successful');
        } else {
            console.log('❌ Product creation failed:', createResult.error);
            return false;
        }
        
        // Get all products
        const getResult = await testAPI('GET', '/products');
        if (getResult.success && getResult.data.length > 0) {
            console.log('✅ Product retrieval successful');
        } else {
            console.log('❌ Product retrieval failed');
            return false;
        }
        
        // Update product
        const updateData = { name: 'Premium Tomatoes', price: 7.99 };
        const updateResult = await testAPI('PUT', `/products/${productId}`, updateData, farmerToken);
        if (updateResult.success) {
            console.log('✅ Product update successful');
            return true;
        } else {
            console.log('❌ Product update failed:', updateResult.error);
            return false;
        }
    },

    async testOrderManagement() {
        console.log('🔍 Testing order management...');
        
        const orderData = {
            products: [{ id: productId, quantity: 5 }]
        };
        
        const createResult = await testAPI('POST', '/orders', orderData, buyerToken);
        if (createResult.success) {
            console.log('✅ Order creation successful');
            
            // Get orders
            const getResult = await testAPI('GET', '/orders', null, buyerToken);
            if (getResult.success && getResult.data.length > 0) {
                console.log('✅ Order retrieval successful');
                return true;
            } else {
                console.log('❌ Order retrieval failed');
                return false;
            }
        } else {
            console.log('❌ Order creation failed:', createResult.error);
            return false;
        }
    },

    async testMessaging() {
        console.log('🔍 Testing messaging system...');
        
        // Get farmer profile to get farmer ID
        const profileResult = await testAPI('GET', '/users/profile', null, farmerToken);
        if (!profileResult.success) {
            console.log('❌ Failed to get farmer profile');
            return false;
        }
        
        const farmerId = profileResult.data.id;
        
        const messageData = {
            receiver_id: farmerId,
            content: 'Hello! I am interested in your tomatoes.'
        };
        
        const sendResult = await testAPI('POST', '/messages', messageData, buyerToken);
        if (sendResult.success) {
            console.log('✅ Message sending successful');
            
            // Get messages
            const getResult = await testAPI('GET', `/messages/${farmerId}`, null, buyerToken);
            if (getResult.success && getResult.data.length > 0) {
                console.log('✅ Message retrieval successful');
                return true;
            } else {
                console.log('❌ Message retrieval failed');
                return false;
            }
        } else {
            console.log('❌ Message sending failed:', sendResult.error);
            return false;
        }
    },

    async testRatingSystem() {
        console.log('🔍 Testing rating system...');
        
        // Get farmer profile
        const profileResult = await testAPI('GET', '/users/profile', null, farmerToken);
        const farmerId = profileResult.data.id;
        
        const ratingData = {
            farmer_id: farmerId,
            product_id: productId,
            score: 8,
            comment: 'Excellent quality tomatoes!'
        };
        
        const result = await testAPI('POST', '/ratings', ratingData, buyerToken);
        if (result.success) {
            console.log('✅ Rating submission successful');
            return true;
        } else {
            console.log('❌ Rating submission failed:', result.error);
            return false;
        }
    },

    async testLeaderboard() {
        console.log('🔍 Testing leaderboard...');
        
        const result = await testAPI('GET', '/leaderboard');
        if (result.success) {
            console.log('✅ Leaderboard retrieval successful');
            return true;
        } else {
            console.log('❌ Leaderboard retrieval failed:', result.error);
            return false;
        }
    },

    async testProfileManagement() {
        console.log('🔍 Testing profile management...');
        
        // Get profile
        const getResult = await testAPI('GET', '/users/profile', null, farmerToken);
        if (!getResult.success) {
            console.log('❌ Profile retrieval failed');
            return false;
        }
        
        // Update profile
        const updateData = { name: 'Updated Farmer Name' };
        const updateResult = await testAPI('PUT', '/users/profile', updateData, farmerToken);
        if (updateResult.success) {
            console.log('✅ Profile update successful');
            return true;
        } else {
            console.log('❌ Profile update failed:', updateResult.error);
            return false;
        }
    },

    async testErrorHandling() {
        console.log('🔍 Testing error handling...');
        
        // Test invalid login
        const invalidLogin = await testAPI('POST', '/login', {
            email: 'invalid@email.com',
            password: 'wrongpassword'
        });
        
        if (!invalidLogin.success && invalidLogin.status === 401) {
            console.log('✅ Invalid login properly rejected');
        } else {
            console.log('❌ Invalid login not properly handled');
            return false;
        }
        
        // Test unauthorized access
        const unauthorizedAccess = await testAPI('POST', '/products', {
            name: 'Test Product',
            price: 10,
            category: 'Test',
            stock: 5
        });
        
        if (!unauthorizedAccess.success && unauthorizedAccess.status === 422) {
            console.log('✅ Unauthorized access properly rejected');
            return true;
        } else {
            console.log('❌ Unauthorized access not properly handled');
            return false;
        }
    }
};

// Run all tests
async function runAllTests() {
    console.log('🚀 Starting Farm Produce Marketplace API Tests\n');
    
    const testResults = [];
    let passedTests = 0;
    
    for (const [testName, testFunction] of Object.entries(tests)) {
        console.log(`\n--- ${testName} ---`);
        try {
            const result = await testFunction();
            testResults.push({ name: testName, passed: result });
            if (result) passedTests++;
            
            // Small delay between tests
            await delay(500);
        } catch (error) {
            console.log(`❌ ${testName} threw an error:`, error.message);
            testResults.push({ name: testName, passed: false });
        }
    }
    
    // Print summary
    console.log('\n' + '='.repeat(50));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(50));
    
    testResults.forEach(result => {
        const status = result.passed ? '✅ PASS' : '❌ FAIL';
        console.log(`${status} ${result.name}`);
    });
    
    console.log(`\n📈 Results: ${passedTests}/${testResults.length} tests passed`);
    
    if (passedTests === testResults.length) {
        console.log('🎉 All tests passed! The API is working correctly.');
    } else {
        console.log('⚠️  Some tests failed. Please check the API implementation.');
    }
    
    return passedTests === testResults.length;
}

// Check if axios is available
try {
    require('axios');
    runAllTests().catch(console.error);
} catch (error) {
    console.log('❌ axios is required to run these tests.');
    console.log('Install it with: npm install axios');
    console.log('Or run: cd client && npm install && cd .. && node test_frontend.js');
}