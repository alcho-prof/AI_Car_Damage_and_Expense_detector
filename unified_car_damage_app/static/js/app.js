document.addEventListener('DOMContentLoaded', () => {
    // State management
    const state = {
        currentImageFile: null,
        currentSampleName: null,
        activeResults: null,
        displayBoxes: true,
        showHighRes: false,
        brandsCatalog: {},
        selectedOutputs: {
            'output-bbox': true,
            'output-severity': true,
            'output-cost': true
        }
    };

    // DOM Elements
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const dropzoneIdle = document.getElementById('dropzone-idle');
    const dropzoneLoading = document.getElementById('dropzone-loading');
    const resultsWrapper = document.getElementById('results-wrapper');

    const brandSelect = document.getElementById('brand-select');
    const modelSelect = document.getElementById('model-select');
    const currencySelect = document.getElementById('currency-select');
    const vehicleTag = document.getElementById('vehicle-tag');

    // Output Toggles (CRITICAL USER REQUIREMENT)
    const toggleBbox = document.getElementById('toggle-bbox');
    const toggleSeverity = document.getElementById('toggle-severity');
    const toggleCost = document.getElementById('toggle-cost');
    const toggleCards = document.querySelectorAll('.output-toggle-card');

    const presetAll = document.getElementById('preset-all');
    const presetBbox = document.getElementById('preset-bbox');
    const presetSeverity = document.getElementById('preset-severity');
    const presetCost = document.getElementById('preset-cost');
    const presetBtns = document.querySelectorAll('.preset-btn');

    const outputBbox = document.getElementById('output-bbox');
    const outputSeverity = document.getElementById('output-severity');
    const outputCost = document.getElementById('output-cost');
    const noModulesNotice = document.getElementById('no-modules-notice');
    const btnShowAllPreset = document.getElementById('btn-show-all-preset');

    // Sample buttons
    const sampleButtons = document.querySelectorAll('.sample-btn');

    // Action buttons
    const btnReanalyze = document.getElementById('btn-reanalyze');
    const btnPrint = document.getElementById('btn-print');
    const btnToggleBoxes = document.getElementById('btn-toggle-boxes');
    const btnViewAnnotated = document.getElementById('btn-view-annotated');

    // ==========================================
    // 1. INITIALIZATION & BRAND DATA FETCHING
    // ==========================================
    async function initBrands() {
        try {
            const res = await fetch('/api/brands');
            const data = await res.json();
            state.brandsCatalog = data.brands || {};

            brandSelect.innerHTML = '';
            Object.keys(state.brandsCatalog).forEach(brand => {
                const opt = document.createElement('option');
                opt.value = brand;
                opt.textContent = brand;
                brandSelect.appendChild(opt);
            });

            // Set default TOYOTA Camry
            if (state.brandsCatalog['TOYOTA']) {
                brandSelect.value = 'TOYOTA';
            }
            updateModelsDropdown();
        } catch (err) {
            console.error('Failed to load brands:', err);
        }
    }

    function updateModelsDropdown() {
        const brand = brandSelect.value;
        const models = state.brandsCatalog[brand] || [];
        modelSelect.innerHTML = '';
        models.forEach(m => {
            const opt = document.createElement('option');
            opt.value = m;
            opt.textContent = m;
            modelSelect.appendChild(opt);
        });
    }

    brandSelect.addEventListener('change', () => {
        updateModelsDropdown();
        if (state.activeResults) {
            triggerAnalysis();
        }
    });

    modelSelect.addEventListener('change', () => {
        if (state.activeResults) {
            triggerAnalysis();
        }
    });

    currencySelect.addEventListener('change', () => {
        if (state.activeResults) {
            triggerAnalysis();
        }
    });

    // ==========================================
    // 2. OUTPUT DISPLAY FILTERING LOGIC
    // "Give it in option for these output. only display the selected display"
    // ==========================================
    function updateOutputVisibility() {
        // Update each module's visibility based on state
        const targets = {
            'output-bbox': { el: outputBbox, toggle: toggleBbox },
            'output-severity': { el: outputSeverity, toggle: toggleSeverity },
            'output-cost': { el: outputCost, toggle: toggleCost }
        };

        Object.keys(targets).forEach(key => {
            const { el, toggle } = targets[key];
            const isVisible = toggle.checked;
            state.selectedOutputs[key] = isVisible;

            const card = document.querySelector(`.output-toggle-card[data-target="${key}"]`);
            if (card) {
                card.classList.toggle('active', isVisible);
            }

            if (isVisible) {
                el.classList.remove('filtered-out');
            } else {
                el.classList.add('filtered-out');
            }
        });

        // Update preset button active state
        const isBbox = toggleBbox.checked;
        const isSev = toggleSeverity.checked;
        const isCost = toggleCost.checked;

        presetBtns.forEach(btn => btn.classList.remove('active'));

        const noneSelected = !isBbox && !isSev && !isCost;
        if (noModulesNotice) {
            noModulesNotice.classList.toggle('hidden', !noneSelected);
        }

        if (isBbox && isSev && isCost) {
            presetAll.classList.add('active');
        } else if (isBbox && !isSev && !isCost) {
            presetBbox.classList.add('active');
        } else if (!isBbox && isSev && !isCost) {
            presetSeverity.classList.add('active');
        } else if (!isBbox && !isSev && isCost) {
            presetCost.classList.add('active');
        }
    }

    if (btnShowAllPreset) {
        btnShowAllPreset.addEventListener('click', () => {
            presetAll.click();
        });
    }

    // Toggle card click listeners
    toggleCards.forEach(card => {
        card.addEventListener('click', (e) => {
            // Prevent double toggle if clicking directly on input
            if (e.target.tagName !== 'INPUT') {
                const input = card.querySelector('input[type="checkbox"]');
                input.checked = !input.checked;
            }
            updateOutputVisibility();
        });
    });

    // Preset button listeners
    presetAll.addEventListener('click', () => {
        toggleBbox.checked = true;
        toggleSeverity.checked = true;
        toggleCost.checked = true;
        updateOutputVisibility();
    });

    presetBbox.addEventListener('click', () => {
        toggleBbox.checked = true;
        toggleSeverity.checked = false;
        toggleCost.checked = false;
        updateOutputVisibility();
    });

    presetSeverity.addEventListener('click', () => {
        toggleBbox.checked = false;
        toggleSeverity.checked = true;
        toggleCost.checked = false;
        updateOutputVisibility();
    });

    presetCost.addEventListener('click', () => {
        toggleBbox.checked = false;
        toggleSeverity.checked = false;
        toggleCost.checked = true;
        updateOutputVisibility();
    });

    // ==========================================
    // 3. FILE UPLOAD & DRAG/DROP
    // ==========================================
    dropzone.addEventListener('click', () => fileInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    function handleFileUpload(file) {
        state.currentImageFile = file;
        state.currentSampleName = null;
        triggerAnalysis();
    }

    // Sample button clicks
    sampleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const sampleName = btn.dataset.sample;
            const brand = btn.dataset.brand;
            const model = btn.dataset.model;

            state.currentSampleName = sampleName;
            state.currentImageFile = null;

            if (brand && state.brandsCatalog[brand]) {
                brandSelect.value = brand;
                updateModelsDropdown();
                if (model) {
                    modelSelect.value = model;
                }
            }

            triggerAnalysis();
        });
    });

    // ==========================================
    // 4. TRIGGER AI DAMAGE ANALYSIS
    // ==========================================
    async function triggerAnalysis() {
        if (!state.currentImageFile && !state.currentSampleName) return;

        dropzoneIdle.classList.add('hidden');
        dropzoneLoading.classList.remove('hidden');

        const formData = new FormData();
        formData.append('brand', brandSelect.value);
        formData.append('model', modelSelect.value);
        formData.append('currency', currencySelect.value);

        if (state.currentSampleName) {
            formData.append('sample_name', state.currentSampleName);
        } else if (state.currentImageFile) {
            formData.append('image', state.currentImageFile);
        }

        try {
            const res = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.error || 'Server error during analysis');
            }

            const data = await res.json();
            state.activeResults = data;
            renderAllResults(data);

            resultsWrapper.classList.remove('hidden');
            resultsWrapper.scrollIntoView({ behavior: 'smooth' });
        } catch (err) {
            alert('Analysis error: ' + err.message);
            console.error(err);
        } finally {
            dropzoneIdle.classList.remove('hidden');
            dropzoneLoading.classList.add('hidden');
        }
    }

    // ==========================================
    // 5. RENDER RESULTS ACROSS THE 3 MODULES
    // ==========================================
    function renderAllResults(data) {
        vehicleTag.textContent = `${data.cost_output.car_brand} ${data.cost_output.car_model}`;

        renderBboxModule(data);
        renderSeverityModule(data);
        renderCostModule(data);

        // Apply current filter visibility
        updateOutputVisibility();
    }

    // --- MODULE 1: Bounding Boxes ---
    function renderBboxModule(data) {
        const imgEl = document.getElementById('analyzed-image');
        const overlay = document.getElementById('bbox-overlay');
        const partsList = document.getElementById('parts-list');
        const totalPill = document.getElementById('total-parts-pill');

        const meta = data.image_metadata;
        const detections = data.bbox_output.detections;

        imgEl.src = state.showHighRes ? meta.annotated_url : meta.original_url;
        totalPill.textContent = `${detections.length} ${detections.length === 1 ? 'Part' : 'Parts'} Detected`;

        // Render client overlay bounding boxes
        overlay.innerHTML = '';
        partsList.innerHTML = '';

        detections.forEach((det, idx) => {
            const b = det.norm_box;
            const rect = document.createElement('div');
            rect.className = `bbox-rect ${det.severity}`;
            rect.style.top = `${b.top}%`;
            rect.style.left = `${b.left}%`;
            rect.style.width = `${b.width}%`;
            rect.style.height = `${b.height}%`;
            rect.dataset.id = det.id;

            const tag = document.createElement('div');
            tag.className = 'bbox-tag';
            tag.textContent = `#${det.id} ${det.part} (${det.confidence_pct}%)`;
            rect.appendChild(tag);
            overlay.appendChild(rect);

            // Parts list item
            const card = document.createElement('div');
            card.className = 'part-card';
            card.dataset.id = det.id;
            card.innerHTML = `
                <div class="part-card-top">
                    <span class="part-card-title">#${det.id} ${det.part}</span>
                    <span class="part-card-badge ${det.severity}">${det.severity}</span>
                </div>
                <div class="part-card-sub">
                    <span>${det.damage_type}</span>
                    <span>Confidence: ${det.confidence_pct}%</span>
                </div>
            `;

            // Hover interactions
            card.addEventListener('mouseenter', () => {
                rect.classList.add('highlighted');
                card.classList.add('active');
            });
            card.addEventListener('mouseleave', () => {
                rect.classList.remove('highlighted');
                card.classList.remove('active');
            });

            rect.addEventListener('mouseenter', () => {
                card.classList.add('active');
                rect.classList.add('highlighted');
            });
            rect.addEventListener('mouseleave', () => {
                card.classList.remove('active');
                rect.classList.remove('highlighted');
            });

            partsList.appendChild(card);
        });
    }

    // Toggle Box layer visibility
    btnToggleBoxes.addEventListener('click', () => {
        state.displayBoxes = !state.displayBoxes;
        document.getElementById('bbox-overlay').style.display = state.displayBoxes ? 'block' : 'none';
        btnToggleBoxes.textContent = state.displayBoxes ? 'Boxes On' : 'Boxes Off';
        btnToggleBoxes.classList.toggle('active', state.displayBoxes);
    });

    // Toggle between original with CSS boxes and OpenCV annotated
    btnViewAnnotated.addEventListener('click', () => {
        state.showHighRes = !state.showHighRes;
        const meta = state.activeResults.image_metadata;
        document.getElementById('analyzed-image').src = state.showHighRes ? meta.annotated_url : meta.original_url;
        btnViewAnnotated.classList.toggle('active', state.showHighRes);
        btnViewAnnotated.textContent = state.showHighRes ? 'Showing Annotated' : 'High-Res Annotated';
        document.getElementById('bbox-overlay').style.display = state.showHighRes ? 'none' : (state.displayBoxes ? 'block' : 'none');
    });

    // --- MODULE 2: Severity Assessment ---
    function renderSeverityModule(data) {
        const sev = data.severity_output;
        const badge = document.getElementById('overall-severity-badge');
        const gaugeVal = document.getElementById('gauge-value');
        const gaugeProg = document.getElementById('gauge-progress');
        const impactLoc = document.getElementById('impact-location');
        const drivable = document.getElementById('drivability-status');
        const structural = document.getElementById('structural-impact');
        const airbag = document.getElementById('airbag-risk');

        badge.className = `severity-badge ${sev.severity_level}`;
        badge.textContent = `${sev.severity_level} (Level ${sev.severity_level === 'Severe' ? '3' : sev.severity_level === 'Moderate' ? '2' : '1'})`;

        gaugeVal.textContent = `${sev.severity_score}%`;
        const offset = 314 - (314 * sev.severity_score / 100);
        gaugeProg.style.strokeDashoffset = offset;

        if (sev.severity_level === 'Severe') {
            gaugeProg.style.stroke = 'var(--accent-rose)';
        } else if (sev.severity_level === 'Moderate') {
            gaugeProg.style.stroke = 'var(--accent-amber)';
        } else {
            gaugeProg.style.stroke = 'var(--accent-emerald)';
        }

        impactLoc.textContent = sev.impact_location;
        drivable.textContent = sev.drivable_status;
        drivable.className = `diag-value status-text ${sev.drivable_badge_color}`;
        structural.textContent = sev.structural_impact;
        airbag.textContent = sev.airbag_risk;
    }

    // --- MODULE 3: Cost Detection ---
    function renderCostModule(data) {
        const cost = data.cost_output;
        const sym = cost.currency_symbol;

        document.getElementById('grand-total-amount').textContent = cost.formatted_grand_total;
        document.getElementById('summary-grand-total').textContent = cost.formatted_grand_total;
        document.getElementById('parts-subtotal').textContent = `${sym}${cost.parts_subtotal.toLocaleString()}`;
        document.getElementById('labor-subtotal').textContent = `${sym}${cost.labor_subtotal.toLocaleString()}`;
        document.getElementById('paint-subtotal').textContent = `${sym}${cost.paint_and_supplies.toLocaleString()}`;
        document.getElementById('tax-subtotal').textContent = `${sym}${cost.estimated_tax.toLocaleString()}`;

        document.getElementById('ins-deductible').textContent = cost.estimated_deductible;
        document.getElementById('ins-payout').textContent = cost.estimated_insurance_coverage;

        const tbody = document.getElementById('cost-table-body');
        tbody.innerHTML = '';

        cost.itemized_parts.forEach((item, idx) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${item.part}</strong></td>
                <td><span style="color: var(--text-secondary);">${item.damage_type}</span></td>
                <td><span class="part-card-badge ${item.severity}">${item.severity}</span></td>
                <td>${item.action}</td>
                <td class="text-right">${sym}${item.part_cost.toLocaleString()}</td>
                <td class="text-right">${sym}${item.labor_cost.toLocaleString()}</td>
                <td class="text-right"><strong style="color: var(--accent-emerald);">${item.formatted_total}</strong></td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Recalculate button
    btnReanalyze.addEventListener('click', () => {
        triggerAnalysis();
    });

    // Print report button
    btnPrint.addEventListener('click', () => {
        window.print();
    });

    // Run on startup
    initBrands();
    updateOutputVisibility();
});
