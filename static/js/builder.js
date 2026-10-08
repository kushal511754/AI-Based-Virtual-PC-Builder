// Builder.js - Main JavaScript for PC Builder interface

let currentBuild = {
    cpu_id: null,
    motherboard_id: null,
    gpu_id: null,
    ram_id: null,
    storage_id: null,
    psu_id: null,
    case_id: null,
    cooling_id: null
};

let components = {
    cpu: [],
    gpu: [],
    motherboard: [],
    ram: [],
    storage: [],
    psu: [],
    case: [],
    cooling: []
};

// Load all components on page load
async function loadComponents() {
    try {
        const [cpus, gpus, motherboards, ram, storage, psus, cases, cooling] = await Promise.all([
            fetch('/api/parts/cpu').then(r => r.json()),
            fetch('/api/parts/gpu').then(r => r.json()),
            fetch('/api/parts/motherboard').then(r => r.json()),
            fetch('/api/parts/ram').then(r => r.json()),
            fetch('/api/parts/storage').then(r => r.json()),
            fetch('/api/parts/psu').then(r => r.json()),
            fetch('/api/parts/case').then(r => r.json()),
            fetch('/api/parts/cooling').then(r => r.json())
        ]);

        components = { cpu: cpus, gpu: gpus, motherboard: motherboards, ram, storage, psu: psus, case: cases, cooling };
        
        populateSelects();
    } catch (e) {
        console.error('Error loading components:', e);
        alert('Error loading components. Please refresh the page.');
    }
}

// Populate all select dropdowns
function populateSelects() {
    populateSelect('cpu-select', components.cpu);
    populateSelect('gpu-select', components.gpu);
    populateSelect('mobo-select', components.motherboard);
    populateSelect('ram-select', components.ram);
    populateSelect('storage-select', components.storage);
    populateSelect('psu-select', components.psu);
    populateSelect('case-select', components.case);
    console.log('COOLING ITEMS TO POPULATE:', components.cooling);
    populateSelect('cooling-select', components.cooling);
}

// Generic function to populate select (Display prices in INR)
function populateSelect(selectId, items) {
    const select = document.getElementById(selectId);
    const options = select.innerHTML; // Keep the default option
    
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        const priceINR = (item.price * 83).toFixed(0);
        option.textContent = `${item.name} - ₹${parseInt(priceINR).toLocaleString('en-IN')}`;
        select.appendChild(option);
    });
}

// Get component details by ID
function getComponentById(category, id) {
    return components[category]?.find(c => c.id === parseInt(id));
}

// Display component info
function displayComponentInfo(category, componentId) {
    const infoId = category === 'motherboard' ? 'mobo-info' : `${category}-info`;
    const infoDiv = document.getElementById(infoId);
    
    if (!componentId) {
        infoDiv.innerHTML = '';
        return;
    }
    
    const component = getComponentById(category, componentId);
    if (!component) return;
    
    let infoHtml = '<div class="component-details">';
    
    switch (category) {
        case 'cpu':
            infoHtml += `
                <p><strong>${component.cores} Cores</strong> / ${component.threads} Threads</p>
                <p>${component.base_clock} - ${component.turbo_clock} GHz</p>
                <p>TDP: ${component.tdp}W | Socket: ${component.socket_type}</p>
            `;
            break;
        case 'gpu':
            infoHtml += `
                <p><strong>${component.vram_gb}GB</strong> ${component.vram_type}</p>
                <p>Memory Speed: ${component.memory_speed_mhz} MHz</p>
                <p>Power Draw: ${component.power_draw}W | Length: ${component.length_mm}mm</p>
            `;
            break;
        case 'motherboard':
            infoHtml += `
                <p><strong>${component.chipset}</strong> Chipset</p>
                <p>Socket: ${component.socket_type} | RAM: ${component.ram_type}</p>
                <p>Max RAM: ${component.max_ram_gb}GB | Form Factor: ${component.form_factor}</p>
            `;
            break;
        case 'ram':
            infoHtml += `
                <p><strong>${component.size_gb}GB</strong> ${component.type}</p>
                <p>Speed: ${component.speed_mhz} MHz | ${component.modules} Modules</p>
            `;
            break;
        case 'storage':
            infoHtml += `
                <p><strong>${component.capacity_gb}GB</strong> ${component.type}</p>
            `;
            break;
        case 'psu':
            infoHtml += `
                <p><strong>${component.wattage}W</strong> Power</p>
                <p>Efficiency: ${component.efficiency_rating} | Modular: ${component.modular ? 'Yes' : 'No'}</p>
            `;
            break;
        case 'case':
            infoHtml += `
                <p><strong>${component.form_factor}</strong> Form Factor</p>
                <p>Max GPU Length: ${component.max_gpu_length_mm}mm</p>
                <p>Max PSU: ${component.max_psu_wattage}W</p>
            `;
            break;
        case 'cooling':
            infoHtml += `
                <p><strong>${component.type}</strong> Cooling</p>
                <p>Socket: ${component.socket_type} | TDP Rating: ${component.tdp_rating}W</p>
            `;
            break;
    }
    
    infoHtml += '</div>';
    infoDiv.innerHTML = infoHtml;
}

// Event listeners for component selection
document.addEventListener('DOMContentLoaded', () => {
    loadComponents();
    
    document.getElementById('cpu-select').addEventListener('change', (e) => {
        currentBuild.cpu_id = e.target.value ? parseInt(e.target.value) : null;
        displayComponentInfo('cpu', e.target.value);
        updateBuild();
    });
    
    document.getElementById('gpu-select').addEventListener('change', (e) => {
        currentBuild.gpu_id = e.target.value ? parseInt(e.target.value) : null;
        displayComponentInfo('gpu', e.target.value);
        updateBuild();
    });
    
    document.getElementById('mobo-select').addEventListener('change', (e) => {
        currentBuild.motherboard_id = e.target.value ? parseInt(e.target.value) : null;
        displayComponentInfo('motherboard', e.target.value);
        updateBuild();
    });
    
    document.getElementById('ram-select').addEventListener('change', (e) => {
        currentBuild.ram_id = e.target.value ? parseInt(e.target.value) : null;
        displayComponentInfo('ram', e.target.value);
        updateBuild();
    });
    
    document.getElementById('storage-select').addEventListener('change', (e) => {
        currentBuild.storage_id = e.target.value ? parseInt(e.target.value) : null;
        displayComponentInfo('storage', e.target.value);
        updateBuild();
    });
    
    document.getElementById('psu-select').addEventListener('change', (e) => {
        currentBuild.psu_id = e.target.value ? parseInt(e.target.value) : null;
        displayComponentInfo('psu', e.target.value);
        updateBuild();
    });
    
    document.getElementById('case-select').addEventListener('change', (e) => {
        currentBuild.case_id = e.target.value ? parseInt(e.target.value) : null;
        displayComponentInfo('case', e.target.value);
        updateBuild();
    });
    
    document.getElementById('cooling-select').addEventListener('change', (e) => {
        console.log('COOLING SELECT CHANGED:', e.target.value);
        currentBuild.cooling_id = e.target.value ? parseInt(e.target.value) : null;
        displayComponentInfo('cooling', e.target.value);
        updateBuild();
    });
    
    document.getElementById('save-build-btn').addEventListener('click', () => {
        if (!currentBuild.cpu_id || !currentBuild.motherboard_id) {
            alert('Please select at least a CPU and Motherboard');
            return;
        }
        document.getElementById('save-modal').classList.remove('hidden');
    });
    
    document.getElementById('clear-build-btn').addEventListener('click', () => {
        if (confirm('Clear all components?')) {
            currentBuild = {
                cpu_id: null,
                motherboard_id: null,
                gpu_id: null,
                ram_id: null,
                storage_id: null,
                psu_id: null,
                case_id: null,
                cooling_id: null
            };
            document.querySelectorAll('.component-input').forEach(input => input.value = '');
            document.querySelectorAll('.component-info').forEach(info => info.innerHTML = '');
            updateBuild();
        }
    });
});

// Update build analysis (compatibility and pricing)
async function updateBuild() {
    try {
        // Check compatibility
        const compatResponse = await fetch('/api/build/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentBuild)
        });
        const compatResult = await compatResponse.json();
        
        // Get pricing
        const priceResponse = await fetch('/api/build/price', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentBuild)
        });
        const priceResult = await priceResponse.json();
        
        // Update UI
        updateCompatibilityDisplay(compatResult);
        updatePricingDisplay(priceResult);
    } catch (e) {
        console.error('Error updating build:', e);
    }
}

// Display compatibility check results
function updateCompatibilityDisplay(result) {
    const compatDiv = document.getElementById('compatibility-status');
    
    if (!currentBuild.cpu_id || !currentBuild.motherboard_id) {
        compatDiv.innerHTML = '<p>Select CPU and Motherboard to check compatibility</p>';
        return;
    }
    
    let html = '<div class="compatibility-result">';
    
    if (result.compatible) {
        html += '<div class="alert alert-success">✓ All components are compatible and fully functional</div>';
    } else {
        html += '<div class="alert alert-error">✗ Build has issues</div>';
    }
    
    if (result.errors && result.errors.length > 0) {
        html += '<div class="errors"><h4>Errors:</h4><ul>';
        result.errors.forEach(err => {
            html += `<li>${err}</li>`;
        });
        html += '</ul></div>';
    }
    
    if (result.warnings && result.warnings.length > 0) {
        html += '<div class="warnings"><h4>Warnings:</h4><ul>';
        result.warnings.forEach(warn => {
            html += `<li>${warn}</li>`;
        });
        html += '</ul></div>';
    }
    
    html += '</div>';
    compatDiv.innerHTML = html;
    
    // Display components breakdown
    displayComponentsBreakdown(result);
}

// Display pricing information
function updatePricingDisplay(result) {
    // Convert USD to INR (1 USD ≈ 83 INR)
    const totalPriceINR = (result.total_price * 83).toFixed(0);
    document.getElementById('total-price').textContent = `₹${parseInt(totalPriceINR).toLocaleString('en-IN')}`;
    
    // Price breakdown
    let breakdownHtml = '';
    for (const [category, price] of Object.entries(result.breakdown)) {
        const priceINR = (price * 83).toFixed(0);
        breakdownHtml += `<div class="breakdown-item"><span>${capitalize(category)}</span><span>₹${parseInt(priceINR).toLocaleString('en-IN')}</span></div>`;
    }
    document.getElementById('price-breakdown').innerHTML = breakdownHtml || '<p>No components selected</p>';
    
    // Suggestions
    let suggestionsHtml = '';
    if (result.suggestions && result.suggestions.length > 0) {
        suggestionsHtml = '<ul>';
        result.suggestions.forEach(suggestion => {
            suggestionsHtml += `<li>${suggestion}</li>`;
        });
        suggestionsHtml += '</ul>';
    } else {
        suggestionsHtml = '<p>No suggestions at the moment</p>';
    }
    document.getElementById('suggestions').innerHTML = suggestionsHtml;
}

// Display components breakdown with individual cards
function displayComponentsBreakdown(compatResult) {
    const breakdownDiv = document.getElementById('components-breakdown');
    if (!breakdownDiv) return;
    
    let html = '<h3>📦 Components Breakdown</h3><div class="components-grid">';
    
    const categories = [
        { key: 'cpu_id', label: 'PROCESSOR', color: 'red' },
        { key: 'gpu_id', label: 'GRAPHICS CARD', color: 'purple' },
        { key: 'motherboard_id', label: 'MOTHERBOARD', color: 'orange' },
        { key: 'ram_id', label: 'MEMORY', color: 'green' },
        { key: 'storage_id', label: 'STORAGE', color: 'blue' },
        { key: 'psu_id', label: 'POWER SUPPLY', color: 'yellow' },
        { key: 'case_id', label: 'CASE', color: 'indigo' },
        { key: 'cooling_id', label: 'COOLING', color: 'cyan' }
    ];
    
    categories.forEach(cat => {
        const buildKey = cat.key;
        const componentId = currentBuild[buildKey];
        const category = buildKey.replace('_id', '');
        
        html += `<div class="component-card ${cat.color}-border">`;
        html += `<div class="component-header ${cat.color}-text">● ${cat.label}</div>`;
        
        if (componentId) {
            const component = getComponentById(category, componentId);
            if (component) {
                html += `<div class="component-name">${component.name}</div>`;
                html += `<div class="component-specs">${getComponentSpecsSummary(category, component)}</div>`;
                html += `<div class="component-price">$${component.price.toFixed(2)}</div>`;
                html += `<div class="component-status compatible">✓ Compatible</div>`;
            }
        } else {
            html += `<div class="component-missing">⚠ Not Selected</div>`;
        }
        
        html += `</div>`;
    });
    
    html += '</div>';
    breakdownDiv.innerHTML = html;
}

// Get component specs summary
function getComponentSpecsSummary(category, component) {
    let specs = '';
    
    switch(category) {
        case 'cpu':
            specs = `${component.cores} Cores, ${component.threads} Threads, ${component.base_clock}GHz`;
            break;
        case 'gpu':
            specs = `${component.vram_gb}GB ${component.vram_type}, ${component.memory_speed_mhz}MHz`;
            break;
        case 'motherboard':
            specs = `${component.socket_type} Socket, ${component.ram_type}, Max ${component.max_ram_gb}GB RAM`;
            break;
        case 'ram':
            specs = `${component.size_gb}GB, ${component.speed_mhz}MHz, ${component.type}`;
            break;
        case 'storage':
            specs = `${component.capacity_gb}GB ${component.type}`;
            break;
        case 'psu':
            specs = `${component.wattage}W, ${component.efficiency_rating}`;
            break;
        case 'case':
            specs = `${component.form_factor}, Max GPU: ${component.max_gpu_length_mm}mm`;
            break;
        case 'cooling':
            specs = `${component.type}, TDP: ${component.tdp_rating}W`;
            break;
        default:
            specs = 'No specs available';
    }
    
    return specs;
}

// Save build function
async function confirmSaveBuild() {
    const buildName = document.getElementById('build-name-input').value.trim();
    
    if (!buildName) {
        alert('Please enter a build name');
        return;
    }
    
    try {
        const response = await fetch('/api/build/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...currentBuild,
                build_name: buildName,
                total_price: parseFloat(document.getElementById('total-price').textContent.replace('₹', '').replace(/,/g, ''))
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Build saved successfully!');
            closeSaveModal();
            // Optionally redirect to saved builds page
            // window.location.href = '/saved';
        } else {
            alert('Error saving build: ' + result.error);
        }
    } catch (e) {
        alert('Error saving build');
        console.error(e);
    }
}

// Close save modal
function closeSaveModal() {
    document.getElementById('save-modal').classList.add('hidden');
    document.getElementById('build-name-input').value = '';
}
