// Helper to POST { id } to /checkout/item/ and return parsed JSON
// The server is expected to return JSON including an `id` field.

function _getCookie(name) {
  const cookie = document.cookie
    .split(';')
    .map(c => c.trim())
    .find(c => c.startsWith(name + '='));
  if (!cookie) return null;
  return decodeURIComponent(cookie.split('=')[1]);
}

async function getCheckoutItem(id, { timeoutMs = 8000 } = {}) {
  if (!id || typeof id !== 'string') {
    throw new TypeError('getCheckoutItem: id must be a non-empty string');
  }

  const url = '/checkout/item/';
  const csrftoken = _getCookie('csrftoken');

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        ...(csrftoken ? { 'X-CSRFToken': csrftoken } : {}),
      },
      body: JSON.stringify({ id }),
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!res.ok) {
      const text = await res.text().catch(() => '');
      const err = new Error(`Request failed: ${res.status} ${res.statusText}`);
      err.status = res.status;
      err.body = text;
      throw err;
    }

    const contentType = res.headers.get('content-type') || '';
    if (!contentType.includes('application/json')) {
      const text = await res.text();
      const err = new Error('Expected JSON response from /checkout/item/');
      err.body = text;
      throw err;
    }

    const data = await res.json();

    // Ensure returned id exists — the API returns { id: uuid, ... }
    if (!data || !data.id) {
      // Not a fatal error but warn and return the payload so caller can decide
      console.warn('getCheckoutItem: response did not include an `id` field', data);
    }

    return data;
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error(`getCheckoutItem: request timed out after ${timeoutMs}ms`);
    }
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}

// Expose globally for inline usage in templates
window.getCheckoutItem = getCheckoutItem;