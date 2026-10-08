// Test script to verify JSON serialization
const testData = {
    'cpu': {'name': 'Intel Core i5-13600K', 'price': 299.0, 'cores': 14},
    'motherboard': {'name': 'MSI MAG B760 TOMAHAWK', 'price': 199.0, 'chipset': 'B760'},
    'gpu': {'name': 'AMD Radeon RX 7800 XT', 'price': 649.0, 'vram_gb': 16},
    'ram': {'name': 'Corsair Vengeance DDR5', 'price': 169.99, 'size_gb': 32}
};

console.log('=== JSON SERIALIZATION TEST ===');
console.log('Original testData:', testData);
console.log('');

// Simulate JSON round-trip
const jsonStr = JSON.stringify(testData);
console.log('After JSON.stringify:', jsonStr);
console.log('');

const parsed = JSON.parse(jsonStr);
console.log('After JSON.parse:', parsed);
console.log('parsed.motherboard:', parsed.motherboard);
console.log('parsed.motherboard.name:', parsed.motherboard.name);
console.log('parsed.motherboard check:', parsed.motherboard && typeof parsed.motherboard === 'object' && parsed.motherboard.name);
