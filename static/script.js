// Smart Bin App - Main JavaScript

// Global state
let currentLanguage = localStorage.getItem('language') || 'en';

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    // Set language selector if it exists
    const langSelect = document.getElementById('languageSelect');
    if (langSelect) {
        langSelect.value = currentLanguage;
    }
});

// Language Management
function changeLanguage(lang) {
    currentLanguage = lang;
    localStorage.setItem('language', lang);
    // In a real app, this would trigger translation of the UI
    showNotification('Language changed to ' + lang, 'success');
}

// Dashboard Actions
function requestPickup() {
    fetch('/api/request-pickup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
        }
    })
    .catch(err => {
        console.error('Error:', err);
        showNotification('Failed to request pickup', 'error');
    });
}

function reportIssue() {
    const issue = prompt("Please describe the issue:");
    if (!issue) return;

    fetch('/api/report-issue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ issue: issue })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
        }
    })
    .catch(err => {
        console.error('Error:', err);
        showNotification('Failed to report issue', 'error');
    });
}

function schedulePickup() {
    const date = prompt("Enter date (YYYY-MM-DD):");
    if (!date) return;
    const time = prompt("Enter time (HH:MM):");
    if (!time) return;

    fetch('/api/schedule-pickup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: date, time: time })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
        }
    })
    .catch(err => {
        console.error('Error:', err);
        showNotification('Failed to schedule pickup', 'error');
    });
}

function sendAlert() {
    const message = prompt("Enter alert message for Ward Authority:");
    if (!message) return;

    fetch('/api/ward-alert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
        }
    })
    .catch(err => {
        console.error('Error:', err);
        showNotification('Failed to send alert', 'error');
    });
}

// Authentication
function logout() {
    fetch('/api/logout', { method: 'POST' })
        .then(() => window.location.href = '/');
}

// UI Helpers
function showNotification(message, type = 'success') {
    const resultDiv = document.getElementById('result');
    const resultMessage = document.getElementById('resultMessage');
    
    if (resultDiv && resultMessage) {
        resultMessage.textContent = message;
        resultDiv.className = `result-card ${type}`;
        resultDiv.style.display = 'flex';
        
        // Change icon based on type
        const icon = resultDiv.querySelector('i');
        if (icon) {
            icon.className = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
        }
        
        setTimeout(() => {
            resultDiv.style.display = 'none';
        }, 5000);
    } else {
        alert(message);
    }
}

// ====== UTILITY FUNCTIONS ======

// Load Notifications
function loadNotifications() {
    const container = document.getElementById('notificationsList');
    if (!container) return;
    
    fetch('/api/notifications')
    .then(res => res.json())
    .then(data => {
        if (data.success && data.notifications.length > 0) {
            container.innerHTML = data.notifications.map(n => `
                <div style="padding: 10px; margin-bottom: 8px; background: ${n.priority === 'high' ? 'rgba(255,0,0,0.1)' : 'rgba(255,255,255,0.05)'}; border-radius: 5px; border-left: 3px solid ${n.type === 'electricity' ? '#ffc107' : n.type === 'water' ? '#0dcaf0' : '#6c757d'};">
                    <div style="font-weight: bold; font-size: 0.9rem;">${n.title}</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary);">${n.message}</div>
                    <div style="font-size: 0.7rem; color: var(--text-secondary); margin-top: 5px;">${n.date}</div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<div style="padding: 10px; text-align: center; color: var(--text-secondary);">No notifications</div>';
        }
    })
    .catch(err => console.error('Error loading notifications:', err));
}

// Load Electricity Schedule
function loadElectricitySchedule() {
    const container = document.getElementById('electricitySchedule');
    if (!container) return;
    
    fetch('/api/electricity-schedule')
    .then(res => res.json())
    .then(data => {
        if (data.success && data.schedule.length > 0) {
            container.innerHTML = data.schedule.slice(0, 5).map(s => `
                <div style="padding: 10px; margin-bottom: 8px; background: rgba(255,193,7,0.1); border-radius: 5px;">
                    <div style="font-weight: bold;"><i class="fas fa-map-marker-alt"></i> ${s.area}</div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">
                        <i class="fas fa-clock"></i> ${s.from_time} - ${s.to_time}
                    </div>
                    <div style="font-size: 0.8rem; color: #ffc107;">${s.reason}</div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<div style="padding: 10px; text-align: center; color: var(--text-secondary);">No scheduled outages</div>';
        }
    })
    .catch(err => console.error('Error loading electricity schedule:', err));
}

// Load Water Schedule
function loadWaterSchedule() {
    const container = document.getElementById('waterSchedule');
    if (!container) return;
    
    fetch('/api/water-schedule')
    .then(res => res.json())
    .then(data => {
        if (data.success && data.schedule.length > 0) {
            container.innerHTML = data.schedule.slice(0, 5).map(s => `
                <div style="padding: 10px; margin-bottom: 8px; background: rgba(13,202,240,0.1); border-radius: 5px;">
                    <div style="font-weight: bold;"><i class="fas fa-map-marker-alt"></i> ${s.area}</div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">
                        <i class="fas fa-clock"></i> ${s.from_time} - ${s.to_time}
                    </div>
                    <div style="font-size: 0.8rem; color: #0dcaf0;">${s.status}</div>
                </div>
            `).join('');
        } else {
            container.innerHTML = '<div style="padding: 10px; text-align: center; color: var(--text-secondary);">No schedule available</div>';
        }
    })
    .catch(err => console.error('Error loading water schedule:', err));
}

// Show Electricity Report Form
function showElectricityReport() {
    const ward = prompt("Enter your Ward (e.g., Ward 1, Ward 2):");
    if (!ward) return;
    
    const issue = prompt("Select issue type:\n1. Power Cut\n2. Low Voltage\n3. Frequent Outages\n4. Line Fault\n5. Other");
    if (!issue) return;
    
    const issueMap = {
        '1': 'Power Cut',
        '2': 'Low Voltage',
        '3': 'Frequent Outages',
        '4': 'Line Fault',
        '5': 'Other'
    };
    
    const description = prompt("Describe the problem:");
    if (!description) return;
    
    const phone = prompt("Enter your phone number for contact:");
    if (!phone) return;
    
    fetch('/api/report-electricity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            ward: ward, 
            issue: issueMap[issue] || issue,
            description: description,
            phone: phone
        })
    })
    .then(res => res.json())
    .then(data => {
        showNotification(data.message, 'success');
    })
    .catch(err => {
        console.error('Error:', err);
        showNotification('Failed to report electricity problem', 'error');
    });
}

// Show Water Report Form
function showWaterReport() {
    const ward = prompt("Enter your Ward (e.g., Ward 1, Ward 2):");
    if (!ward) return;
    
    const issue = prompt("Select issue type:\n1. No Water Supply\n2. Low Pressure\n3. Leakage\n4. Dirty Water\n5. Other");
    if (!issue) return;
    
    const issueMap = {
        '1': 'No Water Supply',
        '2': 'Low Pressure',
        '3': 'Leakage',
        '4': 'Dirty Water',
        '5': 'Other'
    };
    
    const description = prompt("Describe the problem:");
    if (!description) return;
    
    const phone = prompt("Enter your phone number for contact:");
    if (!phone) return;
    
    fetch('/api/report-water', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            ward: ward, 
            issue: issueMap[issue] || issue,
            description: description,
            phone: phone
        })
    })
    .then(res => res.json())
    .then(data => {
        showNotification(data.message, 'success');
    })
    .catch(err => {
        console.error('Error:', err);
        showNotification('Failed to report water problem', 'error');
    });
}

// Auto-load utility data on dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadNotifications();
    loadElectricitySchedule();
    loadWaterSchedule();
});
