/* ═══════════════════════════════════════
   KISANSHAKTI — Main JavaScript
═══════════════════════════════════════ */

// ── Navbar scroll effect
window.addEventListener('scroll', () => {
  const nav = document.getElementById('mainNav');
  if (nav) {
    if (window.scrollY > 50) {
      nav.style.padding = '6px 0';
      nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
    } else {
      nav.style.padding = '12px 0';
      nav.style.boxShadow = 'none';
    }
  }
});

// ── Booking Form Handler
const bookingForm = document.getElementById('bookingForm');
if (bookingForm) {
  bookingForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = bookingForm.querySelector('.btn-submit');
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Submitting...';

    const formData = {
      name:         document.getElementById('customerName').value.trim(),
      mobile:       document.getElementById('mobileNumber').value.trim(),
      village:      document.getElementById('village').value.trim(),
      service:      document.getElementById('serviceType').value,
      acres:        document.getElementById('acres').value,
      booking_date: document.getElementById('bookingDate').value,
    };

    try {
      const response = await fetch('/submit-booking', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (result.success) {
        // Store WhatsApp URL for modal button
        const waBtnModal = document.getElementById('waOpenBtn');
        if (waBtnModal) {
          waBtnModal.href = result.whatsapp_url;
        }

        // Show success modal
        const modal = new bootstrap.Modal(document.getElementById('successModal'));
        modal.show();

        // Reset form
        bookingForm.reset();
      } else {
        showAlert('error', result.message || 'Something went wrong. Please try again.');
      }
    } catch (err) {
      console.error(err);
      showAlert('error', 'Network error. Please check your connection and try again.');
    } finally {
      btn.disabled = false;
      btn.innerHTML = originalText;
    }
  });
}

// ── Alert helper
function showAlert(type, message) {
  const existing = document.getElementById('dynamicAlert');
  if (existing) existing.remove();

  const alertEl = document.createElement('div');
  alertEl.id = 'dynamicAlert';
  alertEl.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show mt-3`;
  alertEl.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;

  const form = document.getElementById('bookingForm');
  if (form) form.insertAdjacentElement('beforebegin', alertEl);

  setTimeout(() => alertEl?.remove(), 5000);
}

// ── Set minimum date for booking form
const dateInput = document.getElementById('bookingDate');
if (dateInput) {
  const today = new Date().toISOString().split('T')[0];
  dateInput.min = today;
}

// ── Intersection Observer for scroll animations
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -40px 0px' };
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Animate cards on scroll
document.querySelectorAll('.service-card, .testimonial-card, .contact-box').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = '0.5s ease';
  observer.observe(el);
});

// ── Active nav link highlight
const currentPath = window.location.pathname;
document.querySelectorAll('.nav-link').forEach(link => {
  if (link.getAttribute('href') === currentPath) {
    link.classList.add('active');
    link.style.color = 'var(--amber)';
  }
});
