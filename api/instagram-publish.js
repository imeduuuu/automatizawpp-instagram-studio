/**
 * ============================================================================
 *  instagram-publish.js  —  Motor de auto-publicación en Instagram
 *  automatizawpp · Instagram Studio
 * ============================================================================
 *
 *  ⚠️  ESTADO: DESACTIVADO POR DISEÑO.
 *
 *  La publicación automática usa la **Instagram Graph API oficial de Meta**.
 *  Para activarla hacen falta (ver memoria: estado_pausa_cnpj):
 *    1. Cuenta de Instagram BUSINESS/CREATOR vinculada a una Página de Facebook.
 *    2. App en Meta for Developers con el permiso `instagram_content_publish`.
 *    3. Verificación de negocio de Meta  → REQUIERE CNPJ (bloqueante actual).
 *
 *  NUNCA se publica con usuario/contraseña automatizando el login: eso viola
 *  las normas de Meta y provoca baneo. Solo vía Graph API oficial.
 *
 *  Mientras IG_PUBLISH_ENABLED !== "true", este módulo NO publica: solo valida
 *  y deja la imagen lista. Así queda integrado en el dashboard pero seguro.
 * ============================================================================
 */

'use strict';

// --- Configuración por variables de entorno (no hardcodear tokens) ---
const CONFIG = {
  ENABLED:      process.env.IG_PUBLISH_ENABLED === 'true',   // gatillo maestro (default OFF)
  IG_USER_ID:   process.env.IG_BUSINESS_USER_ID || '',       // ID de la cuenta IG Business
  ACCESS_TOKEN: process.env.IG_GRAPH_ACCESS_TOKEN || '',     // token de larga duración
  GRAPH_VERSION: process.env.IG_GRAPH_VERSION || 'v21.0',
};

const GRAPH = `https://graph.facebook.com/${CONFIG.GRAPH_VERSION}`;

/**
 * Publica un post en el feed de Instagram.
 * Flujo oficial Graph API (2 pasos):
 *   1) POST /{ig-user-id}/media           → crea un "media container" (image_url + caption)
 *   2) POST /{ig-user-id}/media_publish   → publica el container (creation_id)
 *
 * @param {Object} opts
 * @param {string} opts.imageUrl  URL pública de la imagen (1080x1080).
 * @param {string} opts.caption   Pie de foto (texto + hashtags).
 * @returns {Promise<{ok:boolean, mediaId?:string, reason?:string}>}
 */
async function publishToInstagram({ imageUrl, caption }) {
  // ---- Guardas de seguridad ----
  if (!CONFIG.ENABLED) {
    return { ok: false, reason: 'IG_PUBLISH_ENABLED=false (bloqueado: pendiente CNPJ + verificación Meta).' };
  }
  if (!CONFIG.IG_USER_ID || !CONFIG.ACCESS_TOKEN) {
    return { ok: false, reason: 'Faltan IG_BUSINESS_USER_ID o IG_GRAPH_ACCESS_TOKEN.' };
  }
  if (!imageUrl || !caption) {
    return { ok: false, reason: 'imageUrl y caption son obligatorios.' };
  }

  try {
    // 1) Crear el media container
    const createRes = await fetch(`${GRAPH}/${CONFIG.IG_USER_ID}/media`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_url: imageUrl,
        caption,
        access_token: CONFIG.ACCESS_TOKEN,
      }),
    });
    const createData = await createRes.json();
    if (!createData.id) {
      return { ok: false, reason: `Error creando container: ${JSON.stringify(createData)}` };
    }

    // 2) Publicar el container
    const publishRes = await fetch(`${GRAPH}/${CONFIG.IG_USER_ID}/media_publish`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        creation_id: createData.id,
        access_token: CONFIG.ACCESS_TOKEN,
      }),
    });
    const publishData = await publishRes.json();
    if (!publishData.id) {
      return { ok: false, reason: `Error publicando: ${JSON.stringify(publishData)}` };
    }

    return { ok: true, mediaId: publishData.id };
  } catch (err) {
    return { ok: false, reason: `Excepción: ${err.message}` };
  }
}

/**
 * Programa el feed completo (6 posts), uno por día.
 * Cuando ENABLED, se conectaría a un cron (n8n / node-cron) en el droplet.
 * De momento solo simula y reporta qué haría.
 */
async function scheduleFeed(posts /* [{imageUrl, caption}] */) {
  const results = [];
  for (const post of posts) {
    if (!CONFIG.ENABLED) {
      results.push({ caption: post.caption.slice(0, 40) + '…', status: 'DRY-RUN (desactivado)' });
      continue;
    }
    results.push(await publishToInstagram(post));
  }
  return results;
}

module.exports = { publishToInstagram, scheduleFeed, CONFIG };
