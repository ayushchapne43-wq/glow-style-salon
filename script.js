const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('.nav-menu');

menuToggle.addEventListener('click', () => {
  const isOpen = navMenu.classList.toggle('is-open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
  menuToggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
});

document.querySelectorAll('.nav-menu a').forEach((link) => {
  link.addEventListener('click', () => {
    navMenu.classList.remove('is-open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'Open menu');
  });
});

const dateField = document.querySelector('input[type="date"]');
const today = new Date();
today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
dateField.min = today.toISOString().split('T')[0];

const form = document.querySelector('#booking-form');
const status = document.querySelector('.form-status');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const name = formData.get('name').trim();
  const phone = formData.get('phone').trim();
  const service = formData.get('service');
  const date = formData.get('date');

  if (!name || !phone || !service || !date) {
    status.textContent = 'Please complete your name, phone, service, and preferred date.';
    status.className = 'form-status error';
    return;
  }

  status.textContent = 'Sending your request...';
  status.className = 'form-status';

  try {
    const response = await fetch('/api/appointments', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(formData)),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Unable to send your request.');

    status.textContent = result.message;
    status.className = 'form-status success';
    form.reset();
    dateField.min = today.toISOString().split('T')[0];
  } catch (error) {
    status.textContent = error.message || 'Something went wrong. Please try again.';
    status.className = 'form-status error';
  }
});

const revealObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));
