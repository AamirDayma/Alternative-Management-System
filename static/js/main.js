/**
 * Teacher Management System - Main JavaScript File
 * Handles common functionality across all pages
 */

// Global configuration
const TMS = {
    config: {
        autoSaveDelay: 2000,
        fadeDelay: 150,
        toastDuration: 5000,
        refreshInterval: 5 * 60 * 1000, // 5 minutes
    },
    
    // Global state
    state: {
        currentUser: null,
        currentPage: null,
        unsavedChanges: false,
    },
    
    // Initialize the application
    init: function() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupFormValidation();
        this.setupTooltips();
        this.setupConfirmations();
        this.detectCurrentPage();
        
        console.log('TMS: Application initialized');
    },
    
    // Detect current page for page-specific functionality
    detectCurrentPage: function() {
        const path = window.location.pathname;
        if (path.includes('/admin/')) {
            this.state.currentPage = 'admin';
            this.initAdminFeatures();
        } else if (path.includes('/teacher/')) {
            this.state.currentPage = 'teacher';
            this.initTeacherFeatures();
        } else if (path.includes('/student/')) {
            this.state.currentPage = 'student';
            this.initStudentFeatures();
        }
    },
    
    // Setup global event listeners
    setupEventListeners: function() {
        // Handle form submissions with loading states
        document.addEventListener('submit', this.handleFormSubmit.bind(this));
        
        // Handle navigation confirmations for unsaved changes
        window.addEventListener('beforeunload', this.handleBeforeUnload.bind(this));
        
        // Handle keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
        
        // Handle responsive navigation
        this.setupResponsiveNavigation();
        
        // Auto-dismiss alerts
        this.setupAutoDismissAlerts();
    },
    
    // Initialize Bootstrap components
    initializeComponents: function() {
        // Initialize all tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        // Initialize all popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
        
        // Initialize modals with focus management
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('shown.bs.modal', function() {
                const firstInput = this.querySelector('input, select, textarea');
                if (firstInput) firstInput.focus();
            });
        });
    },
    
    // Setup form validation
    setupFormValidation: function() {
        const forms = document.querySelectorAll('.needs-validation');
        forms.forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                    
                    // Focus on first invalid field
                    const firstInvalid = form.querySelector(':invalid');
                    if (firstInvalid) {
                        firstInvalid.focus();
                    }
                }
                form.classList.add('was-validated');
            });
            
            // Real-time validation feedback
            form.addEventListener('input', function(event) {
                if (form.classList.contains('was-validated')) {
                    const field = event.target;
                    if (field.checkValidity()) {
                        field.classList.remove('is-invalid');
                        field.classList.add('is-valid');
                    } else {
                        field.classList.remove('is-valid');
                        field.classList.add('is-invalid');
                    }
                }
            });
        });
    },
    
    // Setup tooltips for better UX
    setupTooltips: function() {
        // Add tooltips to buttons without text
        document.querySelectorAll('button i.fa, .btn i.fa').forEach(icon => {
            const button = icon.closest('button') || icon.closest('.btn');
            if (button && !button.textContent.trim() && !button.hasAttribute('title')) {
                const classes = icon.className;
                let title = 'Action';
                
                if (classes.includes('fa-edit')) title = 'Edit';
                else if (classes.includes('fa-trash')) title = 'Delete';
                else if (classes.includes('fa-eye')) title = 'View';
                else if (classes.includes('fa-check')) title = 'Approve';
                else if (classes.includes('fa-times')) title = 'Reject';
                else if (classes.includes('fa-plus')) title = 'Add';
                else if (classes.includes('fa-download')) title = 'Download';
                else if (classes.includes('fa-print')) title = 'Print';
                
                button.setAttribute('title', title);
                button.setAttribute('data-bs-toggle', 'tooltip');
            }
        });
    },
    
    // Setup confirmation dialogs
    setupConfirmations: function() {
        document.querySelectorAll('[data-confirm]').forEach(element => {
            element.addEventListener('click', function(event) {
                const message = this.getAttribute('data-confirm');
                if (!confirm(message)) {
                    event.preventDefault();
                    event.stopPropagation();
                }
            });
        });
    },
    
    // Handle form submissions with loading states
    handleFormSubmit: function(event) {
        const form = event.target;
        const submitButton = form.querySelector('button[type="submit"]');
        
        if (submitButton) {
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Processing...';
            submitButton.disabled = true;
            
            // Re-enable button if form submission fails
            setTimeout(() => {
                if (submitButton.disabled) {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }
            }, 10000);
        }
        
        this.state.unsavedChanges = false;
    },
    
    // Handle page unload warnings
    handleBeforeUnload: function(event) {
        if (this.state.unsavedChanges) {
            event.preventDefault();
            event.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
            return event.returnValue;
        }
    },
    
    // Handle keyboard shortcuts
    handleKeyboardShortcuts: function(event) {
        // Ctrl/Cmd + S to save forms
        if ((event.ctrlKey || event.metaKey) && event.key === 's') {
            const form = document.querySelector('form');
            if (form) {
                event.preventDefault();
                form.submit();
            }
        }
        
        // Escape to close modals
        if (event.key === 'Escape') {
            const modal = document.querySelector('.modal.show');
            if (modal) {
                bootstrap.Modal.getInstance(modal)?.hide();
            }
        }
    },
    
    // Setup responsive navigation
    setupResponsiveNavigation: function() {
        const navToggler = document.querySelector('.navbar-toggler');
        const navCollapse = document.querySelector('.navbar-collapse');
        
        if (navToggler && navCollapse) {
            // Close navigation when clicking outside
            document.addEventListener('click', function(event) {
                if (!navToggler.contains(event.target) && !navCollapse.contains(event.target)) {
                    const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                    if (bsCollapse && navCollapse.classList.contains('show')) {
                        bsCollapse.hide();
                    }
                }
            });
        }
    },
    
    // Auto-dismiss alerts
    setupAutoDismissAlerts: function() {
        document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
            if (!alert.querySelector('.btn-close')) return;
            
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, this.config.toastDuration);
        });
    },
    
    // Admin-specific features
    initAdminFeatures: function() {
        this.setupTimetableBuilder();
        this.setupBulkActions();
        this.setupDataTables();
        this.setupDashboardRefresh();
    },
    
    // Teacher-specific features
    initTeacherFeatures: function() {
        this.setupTimetableView();
        this.setupLeaveRequestForm();
        this.setupReplacementResponse();
        this.setupScheduleUpdates();
    },
    
    // Student-specific features
    initStudentFeatures: function() {
        this.setupClassSelection();
        this.setupTimetableDisplay();
    },
    
    // Timetable builder for admin
    setupTimetableBuilder: function() {
        if (!document.querySelector('.timetable-table')) return;
        
        // Add drag and drop functionality (basic implementation)
        document.querySelectorAll('.timetable-entry').forEach(entry => {
            entry.draggable = true;
            entry.addEventListener('dragstart', this.handleDragStart.bind(this));
        });
        
        document.querySelectorAll('.timetable-cell').forEach(cell => {
            cell.addEventListener('dragover', this.handleDragOver.bind(this));
            cell.addEventListener('drop', this.handleDrop.bind(this));
        });
    },
    
    // Bulk actions for admin tables
    setupBulkActions: function() {
        const selectAllCheckbox = document.querySelector('#selectAll');
        const itemCheckboxes = document.querySelectorAll('.item-checkbox');
        const bulkActionButtons = document.querySelectorAll('.bulk-action-btn');
        
        if (selectAllCheckbox && itemCheckboxes.length > 0) {
            selectAllCheckbox.addEventListener('change', function() {
                itemCheckboxes.forEach(checkbox => {
                    checkbox.checked = this.checked;
                });
                TMS.updateBulkActionButtons();
            });
            
            itemCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', this.updateBulkActionButtons.bind(this));
            });
        }
    },
    
    // Update bulk action button states
    updateBulkActionButtons: function() {
        const checkedItems = document.querySelectorAll('.item-checkbox:checked');
        const bulkActionButtons = document.querySelectorAll('.bulk-action-btn');
        
        bulkActionButtons.forEach(button => {
            button.disabled = checkedItems.length === 0;
        });
    },
    
    // Enhanced data tables
    setupDataTables: function() {
        document.querySelectorAll('.data-table').forEach(table => {
            // Add search functionality
            const searchInput = table.parentElement.querySelector('.table-search');
            if (searchInput) {
                searchInput.addEventListener('input', function() {
                    TMS.filterTable(table, this.value);
                });
            }
            
            // Add sorting functionality
            table.querySelectorAll('th[data-sortable]').forEach(header => {
                header.style.cursor = 'pointer';
                header.addEventListener('click', function() {
                    TMS.sortTable(table, this.cellIndex, this.dataset.sortType || 'string');
                });
            });
        });
    },
    
    // Dashboard auto-refresh
    setupDashboardRefresh: function() {
        if (document.querySelector('.dashboard-stats')) {
            setInterval(() => {
                this.refreshDashboardStats();
            }, this.config.refreshInterval);
        }
    },
    
    // Timetable view for teachers
    setupTimetableView: function() {
        this.highlightCurrentTimeSlot();
        this.setupPrintFunctionality();
        
        // Update current time highlighting every minute
        setInterval(() => {
            this.highlightCurrentTimeSlot();
        }, 60000);
    },
    
    // Leave request form enhancements
    setupLeaveRequestForm: function() {
        const leaveTypeRadios = document.querySelectorAll('input[name="leave_type"]');
        const timeSelection = document.getElementById('time_selection');
        const startDateInput = document.querySelector('input[name="start_date"]');
        const endDateInput = document.querySelector('input[name="end_date"]');
        
        if (leaveTypeRadios.length > 0) {
            leaveTypeRadios.forEach(radio => {
                radio.addEventListener('change', function() {
                    if (this.value === 'partial_day') {
                        timeSelection?.style.setProperty('display', 'block');
                        if (startDateInput && endDateInput) {
                            endDateInput.value = startDateInput.value;
                            endDateInput.readOnly = true;
                        }
                    } else {
                        timeSelection?.style.setProperty('display', 'none');
                        if (endDateInput) {
                            endDateInput.readOnly = false;
                        }
                    }
                });
            });
        }
        
        // Date validation
        if (startDateInput && endDateInput) {
            startDateInput.addEventListener('change', function() {
                const startDate = new Date(this.value);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                if (startDate < today) {
                    this.setCustomValidity('Start date cannot be in the past');
                } else {
                    this.setCustomValidity('');
                }
                
                // Update end date minimum
                endDateInput.min = this.value;
                if (endDateInput.value && endDateInput.value < this.value) {
                    endDateInput.value = this.value;
                }
            });
        }
    },
    
    // Replacement response handling
    setupReplacementResponse: function() {
        document.querySelectorAll('[data-replacement-action]').forEach(button => {
            button.addEventListener('click', function() {
                const action = this.dataset.replacementAction;
                const replacementId = this.dataset.replacementId;
                
                if (action && replacementId) {
                    TMS.handleReplacementResponse(replacementId, action);
                }
            });
        });
    },
    
    // Schedule updates for teachers
    setupScheduleUpdates: function() {
        // Check for schedule updates every 5 minutes
        setInterval(() => {
            this.checkScheduleUpdates();
        }, this.config.refreshInterval);
    },
    
    // Class selection for students
    setupClassSelection: function() {
        const classSelect = document.getElementById('class_select');
        if (classSelect) {
            classSelect.addEventListener('change', function() {
                if (this.value) {
                    // Add loading state
                    const container = document.querySelector('.timetable-container');
                    if (container) {
                        container.classList.add('loading');
                    }
                }
            });
        }
    },
    
    // Timetable display enhancements
    setupTimetableDisplay: function() {
        this.highlightCurrentTimeSlot();
        this.setupPrintFunctionality();
        
        // Auto-refresh timetable every 5 minutes for real-time updates
        if (document.querySelector('.timetable-table')) {
            setInterval(() => {
                if (!document.hidden) {
                    this.refreshTimetable();
                }
            }, this.config.refreshInterval);
        }
    },
    
    // Highlight current time slot
    highlightCurrentTimeSlot: function() {
        const now = new Date();
        const currentDay = now.getDay(); // 0 = Sunday, 1 = Monday, etc.
        const currentTime = now.getHours() * 60 + now.getMinutes();
        
        // Remove existing highlights
        document.querySelectorAll('.current-time-slot').forEach(cell => {
            cell.classList.remove('current-time-slot');
        });
        
        // Only highlight if it's Monday-Saturday
        if (currentDay >= 1 && currentDay <= 6) {
            const dayColumn = currentDay; // Adjust for Monday = 1
            
            const timeSlots = [
                [8, 0, 8, 45],   [8, 45, 9, 30],  [9, 30, 10, 15], [10, 15, 11, 0],
                [11, 15, 12, 0], [12, 0, 12, 45], [12, 45, 13, 30], [13, 30, 14, 15], [14, 15, 15, 0]
            ];
            
            timeSlots.forEach((slot, index) => {
                const startTime = slot[0] * 60 + slot[1];
                const endTime = slot[2] * 60 + slot[3];
                
                if (currentTime >= startTime && currentTime <= endTime) {
                    const table = document.querySelector('.timetable-table');
                    if (table) {
                        const rows = table.querySelectorAll('tbody tr');
                        const currentRow = rows[index];
                        const currentCell = currentRow?.cells[dayColumn];
                        
                        if (currentCell) {
                            currentCell.classList.add('current-time-slot');
                            
                            // Add "NOW" indicator if not already present
                            if (!currentCell.querySelector('.current-time-indicator')) {
                                const indicator = document.createElement('div');
                                indicator.className = 'current-time-indicator';
                                indicator.innerHTML = '<i class="fas fa-play"></i> NOW';
                                currentCell.style.position = 'relative';
                                currentCell.appendChild(indicator);
                            }
                        }
                    }
                }
            });
        }
    },
    
    // Print functionality
    setupPrintFunctionality: function() {
        window.printTimetable = function() {
            // Add print-specific class to body
            document.body.classList.add('printing');
            
            // Trigger print
            window.print();
            
            // Remove print class after printing
            setTimeout(() => {
                document.body.classList.remove('printing');
            }, 1000);
        };
    },
    
    // Utility functions
    
    // Filter table rows
    filterTable: function(table, searchTerm) {
        const rows = table.querySelectorAll('tbody tr');
        const term = searchTerm.toLowerCase();
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(term) ? '' : 'none';
        });
    },
    
    // Sort table by column
    sortTable: function(table, columnIndex, dataType) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.sort((a, b) => {
            const aVal = a.cells[columnIndex].textContent.trim();
            const bVal = b.cells[columnIndex].textContent.trim();
            
            if (dataType === 'number') {
                return parseFloat(aVal) - parseFloat(bVal);
            } else if (dataType === 'date') {
                return new Date(aVal) - new Date(bVal);
            } else {
                return aVal.localeCompare(bVal);
            }
        });
        
        rows.forEach(row => tbody.appendChild(row));
    },
    
    // Show toast notification
    showToast: function(message, type = 'info', duration = null) {
        const toastContainer = document.querySelector('.toast-container') || this.createToastContainer();
        const toast = this.createToast(message, type);
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast, {
            delay: duration || this.config.toastDuration
        });
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    },
    
    // Create toast container
    createToastContainer: function() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    },
    
    // Create toast element
    createToast: function(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${type} border-0`;
        toast.role = 'alert';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        return toast;
    },
    
    // AJAX helpers
    
    // Handle replacement response
    handleReplacementResponse: function(replacementId, action) {
        if (!confirm(`Are you sure you want to ${action} this replacement request?`)) {
            return;
        }
        
        const formData = new FormData();
        formData.append('response', action);
        
        fetch(`/teacher/replacements/${replacementId}/respond`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showToast(`Replacement request ${action} successfully!`, 'success');
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showToast(data.message || 'An error occurred', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.showToast('Network error occurred', 'danger');
        });
    },
    
    // Refresh dashboard stats
    refreshDashboardStats: function() {
        fetch('/api/dashboard/stats', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            this.updateDashboardStats(data);
        })
        .catch(error => {
            console.error('Error refreshing dashboard stats:', error);
        });
    },
    
    // Update dashboard stats in DOM
    updateDashboardStats: function(stats) {
        Object.keys(stats).forEach(key => {
            const element = document.querySelector(`[data-stat="${key}"]`);
            if (element) {
                element.textContent = stats[key];
            }
        });
    },
    
    // Check for schedule updates
    checkScheduleUpdates: function() {
        fetch('/api/schedule/updates', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.hasUpdates) {
                this.showToast('Your schedule has been updated. Refresh to see changes.', 'info');
            }
        })
        .catch(error => {
            console.error('Error checking schedule updates:', error);
        });
    },
    
    // Refresh timetable
    refreshTimetable: function() {
        const classId = new URLSearchParams(window.location.search).get('class_id');
        if (!classId) return;
        
        fetch(`/api/timetable/${classId}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.lastUpdated && data.lastUpdated > this.lastTimetableUpdate) {
                this.showToast('Timetable has been updated', 'info');
                this.lastTimetableUpdate = data.lastUpdated;
            }
        })
        .catch(error => {
            console.error('Error refreshing timetable:', error);
        });
    },
    
    // Drag and drop handlers for timetable builder
    handleDragStart: function(event) {
        event.dataTransfer.setData('text/plain', event.target.dataset.entryId || '');
        event.target.style.opacity = '0.5';
    },
    
    handleDragOver: function(event) {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    },
    
    handleDrop: function(event) {
        event.preventDefault();
        const entryId = event.dataTransfer.getData('text/plain');
        const targetCell = event.currentTarget;
        
        // Implementation would depend on backend API for moving timetable entries
        console.log('Drop entry', entryId, 'to cell', targetCell);
        
        // Reset opacity
        document.querySelectorAll('.timetable-entry').forEach(entry => {
            entry.style.opacity = '';
        });
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    TMS.init();
});

// Export for global access
window.TMS = TMS;

// Service Worker registration for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Global error handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    TMS.showToast('An unexpected error occurred', 'danger');
});

// Handle online/offline status
window.addEventListener('online', function() {
    TMS.showToast('Connection restored', 'success');
});

window.addEventListener('offline', function() {
    TMS.showToast('You are now offline', 'warning');
});
