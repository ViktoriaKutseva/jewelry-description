/**
 * Jewelry Calculator Web Application - Main JavaScript
 */

// API Client Class
class ApiClient {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
}

// Material Manager Class
class MaterialManager {
    constructor(apiClient) {
        this.apiClient = apiClient;
        this.selectedMaterials = [];
        this.availableMaterials = [];
        this.materialsContainer = document.getElementById('materialsContainer');
        this.searchInput = null;
        this.filterButtons = null;
        this.selectedMaterialsList = null;
    }

    async initialize() {
        try {
            console.log('Initializing MaterialManager...');
            // Template is now included directly in HTML
            this.setupTemplateElements();
            await this.loadMaterials();
            this.setupEventListeners();
            this.renderMaterials();
            console.log('MaterialManager initialized successfully');
        } catch (error) {
            console.error('Failed to initialize MaterialManager:', error);
            this.showError('Failed to load materials: ' + error.message);
        }
    }

    async loadMaterialsTemplate() {
        try {
            console.log('Loading materials template...');
            const response = await fetch('/static/templates/components/materials.html');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            const template = await response.text();
            console.log('Materials template loaded, length:', template.length);
            if (this.materialsContainer) {
                this.materialsContainer.innerHTML = template;
                this.setupTemplateElements();
                console.log('Materials template applied to DOM');
            } else {
                console.error('Materials container not found');
            }
        } catch (error) {
            console.error('Failed to load materials template:', error);
            this.showError('Failed to load materials component');
        }
    }

    setupTemplateElements() {
        this.searchInput = document.getElementById('materialSearch');
        this.filterButtons = document.querySelectorAll('.filter-btn');
        this.selectedMaterialsList = document.getElementById('selectedMaterialsList');
    }

    async loadMaterials() {
        const materials = await this.apiClient.get('/api/v1/materials');
        this.availableMaterials = materials;
    }

    setupEventListeners() {
        // Search functionality
        if (this.searchInput) {
            this.searchInput.addEventListener('input', (e) => {
                this.filterMaterials(e.target.value);
            });
        }

        // Filter functionality
        if (this.filterButtons) {
            this.filterButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    this.setActiveFilter(e.target);
                    const filter = e.target.dataset.filter;
                    this.filterMaterialsByCategory(filter);
                });
            });
        }
    }

    setActiveFilter(activeButton) {
        this.filterButtons.forEach(button => {
            button.classList.remove('active');
            button.classList.remove('btn-primary');
            button.classList.add('btn-outline-secondary');
        });

        activeButton.classList.add('active');
        activeButton.classList.remove('btn-outline-secondary');
        activeButton.classList.add('btn-primary');
    }

    filterMaterials(searchTerm) {
        const filtered = this.availableMaterials.filter(material =>
            material.name.toLowerCase().includes(searchTerm.toLowerCase())
        );
        this.renderMaterials(filtered);
    }

    filterMaterialsByCategory(category) {
        let filtered = this.availableMaterials;
        if (category && category !== 'all') {
            const categoryMap = {
                'metals': ['gold', 'silver', 'platinum', 'metal'],
                'gems': ['diamond', 'ruby', 'sapphire', 'emerald', 'gem'],
                'other': ['other', 'finding', 'setting']
            };

            filtered = this.availableMaterials.filter(material => {
                const materialCategories = categoryMap[category] || [];
                return materialCategories.some(cat =>
                    material.category?.toLowerCase().includes(cat) ||
                    material.name.toLowerCase().includes(cat)
                );
            });
        }
        this.renderMaterials(filtered);
    }

    renderMaterials(materials = this.availableMaterials) {
        const materialsList = document.getElementById('materialsList');
        if (!materialsList) return;

        if (materials.length === 0) {
            materialsList.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle me-2"></i>
                        No materials found matching your criteria.
                    </div>
                </div>
            `;
            return;
        }

        materialsList.innerHTML = materials.map(material => `
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card material-card h-100" data-material-id="${material.name}">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="card-title mb-0">${material.name}</h6>
                            <span class="badge bg-secondary">${material.category || 'Other'}</span>
                        </div>
                        <p class="card-text text-primary fw-bold mb-2">
                            ${material.unit_price} ₸/${material.unit}
                        </p>
                        <div class="input-group">
                            <input type="number" class="form-control material-quantity"
                                   placeholder="Quantity" min="0" step="0.1">
                            <span class="input-group-text">${material.unit}</span>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        // Add click handlers for material selection
        materialsList.querySelectorAll('.material-card').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.classList.contains('material-quantity')) {
                    this.toggleMaterialSelection(card);
                }
            });
        });

        // Add input handlers for quantity changes
        materialsList.querySelectorAll('.material-quantity').forEach(input => {
            input.addEventListener('input', (e) => {
                this.updateMaterialQuantity(e.target.closest('.material-card'), e.target.value);
            });
        });
    }

    toggleMaterialSelection(card) {
        const materialName = card.dataset.materialId;
        const isSelected = card.classList.contains('selected');

        if (isSelected) {
            card.classList.remove('selected');
            this.selectedMaterials = this.selectedMaterials.filter(m => m.name !== materialName);
        } else {
            card.classList.add('selected');
            const material = this.availableMaterials.find(m => m.name === materialName);
            if (material) {
                this.selectedMaterials.push({
                    name: material.name,
                    unit_price: material.unit_price,
                    quantity: 0,
                    unit: material.unit,
                    category: material.category
                });
            } else {
                console.error('Material not found:', materialName);
            }
        }

        this.updateSelectedMaterialsDisplay();

        // Trigger calculation update
        if (window.jewelryApp && window.jewelryApp.calculatorManager) {
            window.jewelryApp.calculatorManager.updateCalculation();
        }
    }

    updateMaterialQuantity(card, quantity) {
        const materialName = card.dataset.materialId;
        const material = this.selectedMaterials.find(m => m.name === materialName);

        if (material) {
            material.quantity = parseFloat(quantity) || 0;
        }

        this.updateSelectedMaterialsDisplay();

        // Trigger calculation update
        if (window.jewelryApp && window.jewelryApp.calculatorManager) {
            window.jewelryApp.calculatorManager.updateCalculation();
        }
    }

    updateSelectedMaterialsDisplay() {
        if (!this.selectedMaterialsList) return;

        const selectedWithQuantity = this.selectedMaterials.filter(m => m.quantity > 0);

        if (selectedWithQuantity.length === 0) {
            this.selectedMaterialsList.innerHTML = '<p class="text-muted">No materials selected yet.</p>';
            return;
        }

        this.selectedMaterialsList.innerHTML = selectedWithQuantity.map(material => `
            <div class="selected-material-item">
                <div class="d-flex justify-content-between align-items-center">
                    <span>${material.name}</span>
                    <span class="badge bg-primary">${material.quantity} ${material.unit}</span>
                </div>
                <small class="text-muted">Cost: ${(material.unit_price * material.quantity).toFixed(2)} ₸</small>
            </div>
        `).join('');
    }

    getSelectedMaterials() {
        return this.selectedMaterials.filter(m => m.quantity > 0);
    }

    showError(message) {
        if (window.jewelryApp) {
            window.jewelryApp.showAlert(message, 'danger');
        }
    }
}

// Calculator Manager Class
class CalculatorManager {
    constructor(apiClient) {
        this.apiClient = apiClient;
        this.form = document.getElementById('calculatorFormInner');
        this.calculateBtn = document.getElementById('calculateBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.resultsContainer = document.getElementById('calculatorResults');
        this.isCalculating = false;
    }

    initialize() {
        console.log('Initializing CalculatorManager...');
        // Template is now included directly in HTML
        this.setupFormElements();
        console.log('CalculatorManager initialized successfully');
    }

    async loadCalculatorTemplate() {
        try {
            console.log('Loading calculator template...');
            const response = await fetch('/static/templates/components/calculator.html');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            const template = await response.text();
            console.log('Calculator template loaded, length:', template.length);
            const calculatorFormContainer = document.getElementById('calculatorForm');
            if (calculatorFormContainer) {
                calculatorFormContainer.innerHTML = template;
                this.setupFormElements();
                console.log('Calculator template applied to DOM');
            } else {
                console.error('Calculator form container not found');
            }
        } catch (error) {
            console.error('Failed to load calculator template:', error);
            this.showError('Failed to load calculator form');
        }
    }

    setupFormElements() {
        // Form is already set in constructor
        this.calculateBtn = document.getElementById('calculateBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.setupEventListeners();
    }

    setupEventListeners() {
        if (this.calculateBtn) {
            this.calculateBtn.addEventListener('click', () => this.calculateCost());
        }

        if (this.resetBtn) {
            this.resetBtn.addEventListener('click', () => this.resetForm());
        }

        // Auto-calculate on input changes
        if (this.form) {
            this.form.addEventListener('input', () => this.updateCalculation());
        }
    }

    async updateCalculation() {
        const formData = this.getFormData();
        const materials = window.jewelryApp && window.jewelryApp.materialManager ?
            window.jewelryApp.materialManager.getSelectedMaterials() : [];

        if (!this.isFormValid(formData) || materials.length === 0) {
            this.clearResults();
            return;
        }

        // Debounce auto-calculation
        clearTimeout(this.calculationTimeout);
        this.calculationTimeout = setTimeout(() => {
            this.calculateCost();
        }, 500);
    }

    async calculateCost() {
        if (this.isCalculating) return;

        const formData = this.getFormData();
        const materials = window.jewelryApp && window.jewelryApp.materialManager ?
            window.jewelryApp.materialManager.getSelectedMaterials() : [];

        if (!this.isFormValid(formData)) {
            this.showError('Please fill in all required fields');
            return;
        }

        if (materials.length === 0) {
            this.showError('Please select at least one material');
            return;
        }

        this.isCalculating = true;
        this.setLoadingState(true);

        try {
            const requestData = {
                materials: materials,
                jewelry_type: formData.jewelryType,
                weight: formData.weight,
                labor_cost: formData.laborCost,
                markup: formData.markup,
                complexity: formData.complexity,
                quality: formData.quality,
                include_gemstones: formData.includeGemstones,
                include_findings: formData.includeFindings
            };

            const result = await this.apiClient.post('/api/v1/calculator/calculate', requestData);
            this.displayResults(result);

        } catch (error) {
            this.showError('Calculation failed: ' + error.message);
        } finally {
            this.isCalculating = false;
            this.setLoadingState(false);
        }
    }

    getFormData() {
        if (!this.form) return {};

        const formData = new FormData(this.form);
        return {
            jewelryType: formData.get('jewelry_type'),
            weight: parseFloat(formData.get('weight')) || 0,
            laborCost: parseFloat(formData.get('labor_cost')) || 0,
            markup: parseFloat(formData.get('markup')) || 0,
            complexity: formData.get('complexity') || 'medium',
            quality: formData.get('quality') || 'premium',
            includeGemstones: formData.has('include_gemstones'),
            includeFindings: formData.has('include_findings')
        };
    }

    isFormValid(formData) {
        return formData.jewelryType &&
               formData.weight > 0 &&
               formData.laborCost >= 0 &&
               formData.markup >= 0;
    }

    displayResults(result) {
        if (!this.resultsContainer) return;

        this.resultsContainer.innerHTML = `
            <div class="results-header">
                <h4>Calculation Results</h4>
            </div>
            <div class="results-content">
                <div class="result-highlight mb-4">
                    <div class="total-cost">
                        <h3 class="text-primary mb-0">₸${result.total_cost.toFixed(2)}</h3>
                        <small class="text-muted">Total Cost</small>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6">
                        <h5>Cost Breakdown</h5>
                        <div class="cost-breakdown">
                            ${Object.entries(result.cost_breakdown).map(([key, value]) => `
                                <div class="cost-item d-flex justify-content-between">
                                    <span>${this.formatCostLabel(key)}</span>
                                    <strong>₸${value.toFixed(2)}</strong>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h5>Recommended Prices</h5>
                        <div class="price-recommendations">
                            <div class="price-option">
                                <div class="price-label">Minimum</div>
                                <div class="price-value text-success">₸${result.recommended_prices.minimum.toFixed(2)}</div>
                                <small class="price-note">2x cost</small>
                            </div>
                            <div class="price-option">
                                <div class="price-label">Comfort</div>
                                <div class="price-value text-warning">₸${result.recommended_prices.comfort.toFixed(2)}</div>
                                <small class="price-note">2.5x cost</small>
                            </div>
                            <div class="price-option">
                                <div class="price-label">Premium</div>
                                <div class="price-value text-danger">₸${result.recommended_prices.premium.toFixed(2)}</div>
                                <small class="price-note">3x cost</small>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="recommendation-alert">
                    <div class="alert alert-info">
                        <strong>Recommendation:</strong> ${result.price_comment}
                    </div>
                </div>
            </div>
        `;

        // Trigger description generation
        if (window.jewelryApp && window.jewelryApp.descriptionManager) {
            const materials = window.jewelryApp.materialManager.getSelectedMaterials();
            const formData = this.getFormData();
            window.jewelryApp.descriptionManager.generateDescription(formData.jewelryType, materials);
        }
    }

    formatCostLabel(key) {
        const labels = {
            'materials_cost': 'Materials',
            'labor_cost': 'Labor',
            'markup_cost': 'Markup',
            'total_cost': 'Total'
        };
        return labels[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    clearResults() {
        if (this.resultsContainer) {
            const defaultContent = `
                <div class="results-header">
                    <h4>Calculation Results</h4>
                </div>
                <div class="results-content">
                    <p class="text-muted">Enter your jewelry specifications to see the cost breakdown.</p>
                </div>
            `;
            this.resultsContainer.innerHTML = defaultContent;
        }
    }

    resetForm() {
        if (this.form) {
            this.form.reset();
        }
        this.clearResults();

        // Reset material selections
        if (window.jewelryApp && window.jewelryApp.materialManager) {
            window.jewelryApp.materialManager.selectedMaterials = [];
            window.jewelryApp.materialManager.updateSelectedMaterialsDisplay();
        }

        // Clear description
        if (window.jewelryApp && window.jewelryApp.descriptionManager) {
            window.jewelryApp.descriptionManager.clearDescription();
        }
    }

    setLoadingState(loading) {
        if (this.calculateBtn) {
            this.calculateBtn.disabled = loading;
            this.calculateBtn.innerHTML = loading ?
                '<span class="spinner-border spinner-border-sm me-2"></span>Calculating...' :
                '<i class="bi bi-calculator me-2"></i>Calculate Cost';
        }
    }

    showError(message) {
        if (window.jewelryApp) {
            window.jewelryApp.showAlert(message, 'danger');
        }
    }
}

// Description Manager Class
class DescriptionManager {
    constructor(apiClient) {
        this.apiClient = apiClient;
        this.descriptionContainer = document.getElementById('descriptionContainer');
        this.generateBtn = document.getElementById('generateBtn');
        this.copyBtn = document.getElementById('copyBtn');
        this.descriptionStats = document.getElementById('descriptionStats');
        this.descriptionTimestamp = document.getElementById('descriptionTimestamp');
        this.currentDescription = null;
    }

    initialize() {
        console.log('Initializing DescriptionManager...');
        // Template is now included directly in HTML
        this.setupTemplateElements();
        console.log('DescriptionManager initialized successfully');

        if (this.generateBtn) {
            this.generateBtn.addEventListener('click', () => this.generateDescriptionFromUI());
        }

        if (this.copyBtn) {
            this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        }
    }

    async loadDescriptionTemplate() {
        try {
            console.log('Loading description template...');
            const response = await fetch('/static/templates/components/description.html');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            const template = await response.text();
            console.log('Description template loaded, length:', template.length);
            if (this.descriptionContainer) {
                this.descriptionContainer.innerHTML = template;
                this.setupTemplateElements();
                console.log('Description template applied to DOM');
            } else {
                console.error('Description container not found');
            }
        } catch (error) {
            console.error('Failed to load description template:', error);
            this.showError('Failed to load description component');
        }
    }

    setupTemplateElements() {
        this.generateBtn = document.getElementById('generateBtn');
        this.copyBtn = document.getElementById('copyBtn');
        this.descriptionStats = document.getElementById('descriptionStats');
        this.descriptionTimestamp = document.getElementById('descriptionTimestamp');

        if (this.generateBtn) {
            this.generateBtn.addEventListener('click', () => this.generateDescriptionFromUI());
        }

        if (this.copyBtn) {
            this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        }
    }

    async generateDescriptionFromUI() {
        const materials = window.jewelryApp && window.jewelryApp.materialManager ?
            window.jewelryApp.materialManager.getSelectedMaterials() : [];

        const calculatorData = window.jewelryApp && window.jewelryApp.calculatorManager ?
            window.jewelryApp.calculatorManager.getFormData() : {};

        if (materials.length === 0) {
            this.showError('Please select materials first');
            return;
        }

        await this.generateDescription(calculatorData.jewelryType || 'ring', materials);
    }

    async generateDescription(jewelryType, materials) {
        if (!this.descriptionContainer || materials.length === 0) return;

        this.setLoadingState(true);

        try {
            const materialNames = materials.map(m => m.name);
            const requestData = {
                jewelry_type: jewelryType,
                materials: materialNames
            };

            const result = await this.apiClient.post('/api/v1/descriptions/generate', requestData);
            this.displayDescription(result);
            this.currentDescription = result;

        } catch (error) {
            this.showError('Failed to generate description: ' + error.message);
        } finally {
            this.setLoadingState(false);
        }
    }

    displayDescription(result) {
        const descriptionText = document.getElementById('descriptionText');
        if (!descriptionText) return;

        descriptionText.innerHTML = `
            <div class="description-content">
                <div class="description-text">
                    "${result.description}"
                </div>
                <div class="hashtags mt-3">
                    ${result.hashtags.map(tag => `<span class="badge bg-light text-dark me-1">${tag}</span>`).join('')}
                </div>
            </div>
        `;

        // Update stats
        this.updateStats(result);

        // Update timestamp
        this.updateTimestamp();

        // Enable copy button
        if (this.copyBtn) {
            this.copyBtn.disabled = false;
        }

        // Enable generate button
        if (this.generateBtn) {
            this.generateBtn.disabled = false;
        }
    }

    updateStats(result) {
        if (!this.descriptionStats) return;

        const wordCount = result.description.split(' ').length;
        const charCount = result.description.length;
        const hashtagCount = result.hashtags.length;

        this.descriptionStats.innerHTML = `
            <div class="stats-item">
                <span class="stats-label">Words:</span>
                <span class="stats-value">${wordCount}</span>
            </div>
            <div class="stats-item">
                <span class="stats-label">Characters:</span>
                <span class="stats-value">${charCount}</span>
            </div>
            <div class="stats-item">
                <span class="stats-label">Hashtags:</span>
                <span class="stats-value">${hashtagCount}</span>
            </div>
        `;
    }

    updateTimestamp() {
        if (!this.descriptionTimestamp) return;

        const now = new Date();
        const timestamp = now.toLocaleString();
        this.descriptionTimestamp.innerHTML = `
            <small class="text-muted">Generated: ${timestamp}</small>
        `;
    }

    clearDescription() {
        const descriptionText = document.getElementById('descriptionText');
        if (descriptionText) {
            descriptionText.innerHTML = `
                <div class="description-placeholder">
                    <i class="bi bi-file-text display-4 text-muted"></i>
                    <p class="text-muted mt-3">Complete the calculator above to generate a description.</p>
                </div>
            `;
        }

        if (this.descriptionStats) {
            this.descriptionStats.innerHTML = '';
        }

        if (this.descriptionTimestamp) {
            this.descriptionTimestamp.innerHTML = '';
        }

        if (this.copyBtn) {
            this.copyBtn.disabled = true;
        }

        if (this.generateBtn) {
            this.generateBtn.disabled = true;
        }

        this.currentDescription = null;
    }

    async copyToClipboard() {
        if (!this.currentDescription) {
            this.showError('No description to copy');
            return;
        }

        try {
            const descriptionText = this.currentDescription.description;
            const hashtags = this.currentDescription.hashtags.join(' ');
            const fullText = `${descriptionText}\n\n${hashtags}`;

            await navigator.clipboard.writeText(fullText);

            this.showAlert('Description copied to clipboard!', 'success');

        } catch (error) {
            this.showError('Failed to copy to clipboard');
        }
    }

    setLoadingState(loading) {
        if (this.generateBtn) {
            this.generateBtn.disabled = loading;
            this.generateBtn.innerHTML = loading ?
                '<span class="spinner-border spinner-border-sm me-2"></span>Generating...' :
                '<i class="bi bi-magic me-1"></i>Generate Description';
        }
    }

    showError(message) {
        if (window.jewelryApp) {
            window.jewelryApp.showAlert(message, 'danger');
        }
    }

    showAlert(message, type = 'info') {
        if (window.jewelryApp) {
            window.jewelryApp.showAlert(message, type);
        }
    }
}

// Jewelry Application Main Class
class JewelryApp {
    constructor() {
        this.apiClient = new ApiClient();
        this.materialManager = new MaterialManager(this.apiClient);
        this.calculatorManager = new CalculatorManager(this.apiClient);
        this.descriptionManager = new DescriptionManager(this.apiClient);
        this.alertContainer = document.getElementById('alertContainer');
    }

    async initialize() {
        try {
            console.log('Initializing Jewelry Calculator Web App...');

            // Initialize all managers
            await this.materialManager.initialize();
            this.calculatorManager.initialize();
            this.descriptionManager.initialize();

            // Load initial data
            await this.loadInitialData();

            console.log('Jewelry Calculator Web App initialized successfully!');
        } catch (error) {
            console.error('Failed to initialize application:', error);
            this.showAlert('Failed to initialize application: ' + error.message, 'danger');
        }
    }

    async loadInitialData() {
        try {
            // Check API health
            await this.apiClient.get('/health');
            this.updateStatusIndicator(true);
        } catch (error) {
            console.warn('API health check failed:', error);
            this.updateStatusIndicator(false);
        }
    }

    updateStatusIndicator(isOnline) {
        const statusBadge = document.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.className = `badge ${isOnline ? 'bg-success' : 'bg-danger'} status-badge`;
            statusBadge.innerHTML = `
                <i class="bi ${isOnline ? 'bi-check-circle-fill' : 'bi-x-circle-fill'} me-1"></i>
                ${isOnline ? 'System Online' : 'System Offline'}
            `;
        }
    }

    showAlert(message, type = 'info') {
        if (!this.alertContainer) return;

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        this.alertContainer.appendChild(alertDiv);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}