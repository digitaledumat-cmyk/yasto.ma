#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Yasto.ma static pages with shared chrome."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://yasto.ma"
WA = "https://wa.me/212664140211"
PHONE_DISPLAY = "+212 664-140 211"

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">"""


def asset(path, depth):
    return ("../" * depth) + path


def page_url(file_slug: str) -> str:
    """Map on-disk html path or public path to clean URL: faq.html -> /faq."""
    s = (file_slug or "").strip()
    if s in ("index.html", "index", "", "/"):
        return "/"
    s = s.lstrip("/")
    if s.endswith("/"):
        s = s.rstrip("/")
    if s.endswith("/index.html"):
        s = s[: -len("/index.html")]
    elif s.endswith(".html"):
        s = s[:-5]
    return f"/{s}" if s else "/"


def canonical_url(file_slug: str) -> str:
    u = page_url(file_slug)
    return SITE + "/" if u == "/" else SITE + u


def disk_path(slug: str) -> Path:
    """Map public/legacy slug to on-disk .html path under ROOT."""
    s = (slug or "").strip().lstrip("/")
    if s in ("", "index", "index.html"):
        return ROOT / "index.html"
    if s in ("blog", "blog/", "blog/index.html"):
        return ROOT / "blog" / "index.html"
    if s.endswith("/"):
        s = s.rstrip("/")
    if s.endswith(".html"):
        return ROOT / s
    return ROOT / f"{s}.html"


def head(title, description, canonical, depth=0, extra="", og_type="website"):
    css = asset("css/style.css", depth)
    fav = asset("assets/favicon.png", depth)
    logo = asset("assets/logo-yasto.png", depth)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Yasto.ma">
<meta name="geo.region" content="MA">
<meta name="geo.placename" content="Casablanca, Marrakech, Rabat, Tanger, Agadir, Fès">
<meta name="language" content="fr">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="fr" href="{canonical}">
<link rel="icon" type="image/png" href="{fav}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Yasto.ma">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/logo-yasto.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="keywords" content="IPTV Maroc, abonnement IPTV Maroc, meilleur IPTV Maroc, fournisseur IPTV Maroc, acheter IPTV Maroc, recharge IPTV Maroc, IPTV 4K Maroc, IPTV HD Maroc, IPTV Casablanca, IPTV Marrakech, IPTV Rabat, IPTV Tanger, IPTV Agadir, IPTV Fès, Yasto.ma">
{FONTS}
<link rel="stylesheet" href="{css}">
{extra}
</head>
<body>
<div class="scanlines" aria-hidden="true"></div>"""


def nav(active, depth=0):
    logo = asset("assets/logo-yasto.png", depth)
    pages = [
        ("index.html", "IPTV Maroc", "accueil"),
        ("/abonnement-iptv", "Abonnement IPTV", "abo"),
        ("/guide-installation", "Guide d'installation", "guide"),
        ("/faq", "FAQ", "faq"),
        ("/blog", "Blog", "blog"),
        ("/contact", "Contact", "contact"),
    ]
    items = []
    for href, label, key in pages:
        cls = ' class="active"' if key == active else ""
        items.append(f'<a href="{page_url(href)}"{cls}>{label}</a>')
    links = "\n".join(items)
    return f"""<header class="site-header">
  <div class="container nav">
    <a class="logo" href="{page_url('index.html')}" aria-label="Yasto.ma — Accueil">
      <img src="{logo}" width="42" height="42" alt="Logo Yasto.ma" decoding="async">
      Yasto<span>.ma</span>
    </a>
    <button class="menu-toggle" type="button" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav-links" aria-label="Navigation principale">
      {links}
      <a class="btn btn-primary nav-cta" href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp</a>
    </nav>
  </div>
</header>"""


def footer(depth=0):
    logo = asset("assets/logo-yasto.png", depth)
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a class="logo" href="{page_url('index.html')}">
        <img src="{logo}" width="42" height="42" alt="Yasto.ma" loading="lazy" decoding="async">
        Yasto<span>.ma</span>
      </a>
      <p>Fournisseur <strong>IPTV Maroc</strong> premium — chaînes live, films &amp; séries en HD / 4K. Activation rapide, support 24/7, garantie 45 jours.</p>
    </div>
    <div class="footer-col">
      <h4>Navigation</h4>
      <a href="{page_url('index.html')}">IPTV Maroc</a>
      <a href="{page_url('/abonnement-iptv')}">Abonnement IPTV</a>
      <a href="{page_url('/guide-installation')}">Guide d'installation</a>
      <a href="{page_url('/faq')}">FAQ</a>
      <a href="{page_url('/blog')}">Blog</a>
      <a href="{page_url('/contact')}">Contact</a>
    </div>
    <div class="footer-col">
      <h4>Légal</h4>
      <a href="{page_url('/mentions-legales')}">Mentions légales</a>
      <a href="{page_url('/conditions-utilisation')}">Conditions d'utilisation</a>
      <a href="{page_url('/politique-confidentialite')}">Confidentialité</a>
      <a href="{page_url('/rgpd')}">Conformité RGPD</a>
      <a href="{page_url('/politique-utilisation-acceptable')}">Utilisation acceptable</a>
      <a href="{page_url('/dmca')}">Politique DMCA</a>
      <a href="{page_url('/remboursement')}">Remboursement</a>
    </div>
    <div class="footer-col">
      <h4>Ressources</h4>
      <a href="{page_url('/plan-du-site')}">Plan du site</a>
      <a href="{page_url('/sitemap')}">Sitemap HTML</a>
      <a href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp {PHONE_DISPLAY}</a>
      <a href="mailto:contact@yasto.ma">contact@yasto.ma</a>
    </div>
  </div>
  <div class="container footer-bottom">
    <span>© <span data-year></span> Yasto.ma — IPTV Maroc</span>
    <span>Service digital · Activation sous 5–15 min</span>
  </div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener noreferrer" aria-label="Essai 24h WhatsApp">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-2.772-1.387-3.2-1.587-.428-.2-.74-.297-.974.148-.233.297-.934 1.587-1.146 1.912-.212.297-.424.334-.78.113-.356-.222-1.51-.556-2.876-1.773-1.064-.961-1.783-2.149-1.991-2.513-.208-.334-.022-.515.156-.68.16-.158.357-.412.534-.618.178-.207.237-.349.356-.58.119-.232.06-.434-.03-.608-.09-.173-.974-2.345-1.334-3.213-.351-.867-.708-.748-.974-.762-.25-.012-.534-.014-.82-.014s-.743.105-1.132.508c-.388.403-1.482 1.447-1.482 3.528s1.518 4.092 1.633 4.376c.119.297 2.818 4.301 6.837 6.026 4.02 1.724 4.02 1.15 4.734 1.077.715-.074 2.298-.94 2.623-1.847.325-.908.325-1.686.227-1.847-.097-.16-.356-.254-.653-.403z"/><path d="M12.004 2C6.486 2 2 6.477 2 11.985c0 1.76.46 3.475 1.336 4.992L2 22l5.163-1.353A9.97 9.97 0 0 0 12.004 22C17.52 22 22 17.523 22 12.015 22 6.477 17.52 2 12.004 2zm0 18.15a8.13 8.13 0 0 1-4.14-1.134l-.296-.176-3.063.803.818-2.985-.193-.307A8.12 8.12 0 0 1 3.85 12c0-4.497 3.66-8.15 8.154-8.15 4.493 0 8.146 3.653 8.146 8.15 0 4.49-3.653 8.15-8.146 8.15z"/></svg>
  Essai 24h
</a>
<script src="{asset('js/main.js', depth)}" defer></script>
</body>
</html>"""


def page(title, description, slug, active, body, depth=0, extra="", og_type="website"):
    canonical = canonical_url(slug)
    html = head(title, description, canonical, depth, extra, og_type) + nav(active, depth) + body + footer(depth)
    path = disk_path(slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("Wrote", path.relative_to(ROOT))


# ─── Shared pricing block ───────────────────────────────────────────
PRICING = f"""
<section class="section" id="tarifs">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Tarifs IPTV Maroc</span>
      <h2>Choisir mon abonnement IPTV Maroc</h2>
      <p>Trois packs Premium pour acheter IPTV Maroc en toute confiance. Garantie <strong>45 jours satisfait ou remboursé</strong>. Activation rapide, recharge IPTV Maroc disponible 24/7.</p>
    </div>
    <div class="pricing-grid">
      <article class="price-card">
        <h3>Pro</h3>
        <p class="price-period">IPTV HD Maroc · 1 appareil</p>
        <div class="price-amount">250 <small>DHS</small></div>
        <ul class="price-features">
          <li>+20 000 chaînes TV</li>
          <li>+25 000 films et séries</li>
          <li>Serveur stable</li>
          <li>Résolution HD</li>
          <li>Anti-freeze</li>
          <li>Compatibilité assurée</li>
          <li>Utilisation sur 1 appareil</li>
          <li>Support 24/7</li>
        </ul>
        <a class="btn btn-ghost" href="{WA}" data-pack="Pro" data-price="250">Commander Pro</a>
      </article>
      <article class="price-card featured">
        <span class="price-badge">Meilleur choix</span>
        <h3>Pro+</h3>
        <p class="price-period">Meilleur IPTV Maroc · 2 appareils</p>
        <div class="price-amount">350 <small>DHS</small></div>
        <ul class="price-features">
          <li>+29 000 chaînes TV</li>
          <li>+129 000 films et séries</li>
          <li>Serveur OTT</li>
          <li>Résolution FHD</li>
          <li>Anti-freeze 2.0</li>
          <li>Compatibilité assurée</li>
          <li>Utilisation sur 2 appareils</li>
          <li>Activation application</li>
          <li>Support 24/7</li>
        </ul>
        <a class="btn btn-primary" href="{WA}" data-pack="Pro+" data-price="350">Commander Pro+</a>
      </article>
      <article class="price-card">
        <h3>Pro Premium</h3>
        <p class="price-period">IPTV 4K Maroc · 3 appareils</p>
        <div class="price-amount">450 <small>DHS</small></div>
        <ul class="price-features">
          <li>+45 000 chaînes TV</li>
          <li>+180 000 films et séries</li>
          <li>Serveur OTT VPS</li>
          <li>Résolution 4K UHD</li>
          <li>Anti-freeze 2.2</li>
          <li>Compatibilité assurée</li>
          <li>Utilisation sur 3 appareils</li>
          <li>Activation application PRO</li>
          <li>Support 24/7</li>
        </ul>
        <a class="btn btn-ghost" href="{WA}" data-pack="Pro Premium" data-price="450">Commander Premium</a>
      </article>
    </div>
  </div>
</section>
"""

FORM_TEST = f"""
<section class="section" id="essai-gratuit">
  <div class="container form-section">
    <div>
      <div class="section-head">
        <span class="eyebrow">Essai gratuit 24 heures</span>
        <h2>Demander un test IPTV Maroc gratuit</h2>
        <p>Testez le <strong>meilleur IPTV Maroc</strong> avant d'acheter. Remplissez le formulaire : nous vous envoyons un accès test 24h via WhatsApp. Idéal pour vérifier image, fluidité et chaînes locales (Maroc, France, Espagne, sport, cinéma).</p>
      </div>
      <ul class="price-features" style="margin-top:1rem">
        <li>Test sans engagement · 24 heures</li>
        <li>Activation rapide après validation WhatsApp</li>
        <li>Compatible Smart TV, Android, iOS, Fire Stick, PC</li>
        <li>Support francophone 24/7</li>
      </ul>
    </div>
    <div class="form-panel">
      <form data-whatsapp data-type="test" novalidate>
        <div class="form-grid">
          <div class="form-group">
            <label for="nom">Nom</label>
            <input id="nom" name="nom" type="text" required autocomplete="family-name" placeholder="Alaoui">
          </div>
          <div class="form-group">
            <label for="prenom">Prénom</label>
            <input id="prenom" name="prenom" type="text" required autocomplete="given-name" placeholder="Youssef">
          </div>
          <div class="form-group full">
            <label for="telephone">Numéro de téléphone</label>
            <div class="phone-row">
              <select id="indicatif" name="indicatif" aria-label="Indicatif pays">
                <option value="+212" selected>+212</option>
                <option value="+33">+33</option>
                <option value="+34">+34</option>
                <option value="+1">+1</option>
                <option value="+32">+32</option>
                <option value="+41">+41</option>
              </select>
              <input id="telephone" name="telephone" type="tel" required inputmode="numeric" autocomplete="tel-national" placeholder="6XX XXX XXX" pattern="[0-9\\s\\-]{{8,15}}">
            </div>
          </div>
          <div class="form-group full">
            <label for="abonnement">Choix d'abonnement (optionnel)</label>
            <select id="abonnement" name="abonnement">
              <option value="À définir lors du test">À définir lors du test</option>
              <option value="Pro — 250 DHS">Pro — 250 DHS</option>
              <option value="Pro+ — 350 DHS">Pro+ — 350 DHS</option>
              <option value="Pro Premium — 450 DHS">Pro Premium — 450 DHS</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn btn-whatsapp" type="submit">Envoyer par WhatsApp</button>
          <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener noreferrer">Écrire directement</a>
        </div>
        <p class="form-note">En cliquant, WhatsApp s'ouvre avec votre demande de test IPTV Maroc préremplie. Indicatif Maroc (+212) sélectionné par défaut.</p>
      </form>
    </div>
  </div>
</section>
"""

REVIEWS = """
<section class="section" id="avis">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Preuve sociale</span>
      <h2>Avis clients IPTV Maroc</h2>
      <p><strong>834 avis</strong> 5 étoiles — abonnés au Maroc, en France et en Espagne.</p>
    </div>
    <div class="reviews-meta" style="justify-content:center">
      <span class="stars" aria-hidden="true">★★★★★</span>
      <strong>4,9 / 5</strong>
      <span style="color:var(--text-muted)">basé sur 834 avis vérifiés</span>
    </div>
    <div class="reviews-grid">
      <article class="review">
        <div class="stars">★★★★★</div>
        <p>« Meilleur IPTV Maroc que j'ai testé. Image stable à Casablanca, chaînes beIN et Al Aoula nickel. Activation en 10 min. »</p>
        <div class="review-author">Karim B.</div>
        <div class="review-loc">Casablanca, Maroc</div>
      </article>
      <article class="review">
        <div class="stars">★★★★★</div>
        <p>« Je cherchais un fournisseur IPTV Maroc fiable pour Marrakech. Pro+ est fluide, VOD immense, support WhatsApp réactif. »</p>
        <div class="review-author">Salma M.</div>
        <div class="review-loc">Marrakech, Maroc</div>
      </article>
      <article class="review">
        <div class="stars">★★★★★</div>
        <p>« Desde Valencia miro la Liga y canales marroquíes sin cortes. Recomiendo IPTV 4K Maroc de Yasto.ma. »</p>
        <div class="review-author">Javier R.</div>
        <div class="review-loc">Valence, Espagne</div>
      </article>
      <article class="review">
        <div class="stars">★★★★★</div>
        <p>« À Rabat, Pro Premium en 4K sur Fire Stick. Anti-freeze sérieux. La garantie 45 jours m'a convaincu d'acheter. »</p>
        <div class="review-author">Imane T.</div>
        <div class="review-loc">Rabat, Maroc</div>
      </article>
      <article class="review">
        <div class="stars">★★★★★</div>
        <p>« Français résidant à Lyon : chaînes FR + MA + foot. Abonnement IPTV Maroc clairement au-dessus des offres low-cost. »</p>
        <div class="review-author">Thomas L.</div>
        <div class="review-loc">Lyon, France</div>
      </article>
      <article class="review">
        <div class="stars">★★★★★</div>
        <p>« Tanger, ADSL moyen : serveur stable quand même. Recharge IPTV Maroc simple via WhatsApp. Merci Yasto. »</p>
        <div class="review-author">Yassine K.</div>
        <div class="review-loc">Tanger, Maroc</div>
      </article>
      <article class="review">
        <div class="stars">★★★★★</div>
        <p>« Agadir + Fès chez la famille : 2 appareils Pro+. Très bon rapport qualité/prix pour acheter IPTV Maroc. »</p>
        <div class="review-author">Nadia E.</div>
        <div class="review-loc">Agadir, Maroc</div>
      </article>
      <article class="review">
        <div class="stars">★★★★★</div>
        <p>« Servicio serio, habla francesa y árabe. Canales de fútbol y cine 4K. Volveré a renovar. »</p>
        <div class="review-author">Lucía P.</div>
        <div class="review-loc">Madrid, Espagne</div>
      </article>
      <article class="review">
        <div class="stars">★★★★★</div>
        <p>« IPTV HD Maroc nickel à Oujda. Installation Android TV suivie étape par étape. Support au top. »</p>
        <div class="review-author">Mehdi A.</div>
        <div class="review-loc">Oujda, Maroc</div>
      </article>
    </div>
  </div>
</section>
"""

CITIES = """
<section class="cities" aria-label="Couverture IPTV Maroc par ville">
  <div class="container">
    <div class="section-head center" style="margin-bottom:1.25rem">
      <span class="eyebrow">SEO local</span>
      <h2 style="font-size:1.35rem">IPTV disponible dans tout le Maroc</h2>
      <p>Abonnement IPTV Maroc livré digitalement pour les grandes villes et la diaspora.</p>
    </div>
    <div class="cities-list">
      <span>IPTV Casablanca</span><span>IPTV Marrakech</span><span>IPTV Rabat</span>
      <span>IPTV Tanger</span><span>IPTV Agadir</span><span>IPTV Fès</span>
      <span>IPTV Meknès</span><span>IPTV Oujda</span><span>IPTV Kénitra</span>
      <span>IPTV Tétouan</span><span>IPTV Salé</span><span>IPTV Mohammedia</span>
      <span>IPTV El Jadida</span><span>IPTV Nador</span><span>IPTV Safi</span>
      <span>IPTV Essaouira</span><span>IPTV Beni Mellal</span><span>IPTV Taza</span>
      <span>IPTV Paris</span><span>IPTV Lyon</span><span>IPTV Marseille</span>
      <span>IPTV Madrid</span><span>IPTV Barcelone</span><span>IPTV Valence</span>
    </div>
  </div>
</section>
"""

SCHEMA_HOME = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://yasto.ma/#org",
      "name": "Yasto.ma",
      "url": "https://yasto.ma/",
      "logo": "https://yasto.ma/assets/logo-yasto.png",
      "sameAs": ["https://wa.me/212664140211"],
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+212-664-140-211",
        "contactType": "customer service",
        "availableLanguage": ["French", "Arabic", "Spanish"],
        "areaServed": ["MA", "FR", "ES"]
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://yasto.ma/#website",
      "url": "https://yasto.ma/",
      "name": "Yasto.ma — IPTV Maroc",
      "publisher": {"@id": "https://yasto.ma/#org"},
      "inLanguage": "fr-MA"
    },
    {
      "@type": "Product",
      "name": "Abonnement IPTV Maroc Yasto.ma",
      "description": "Abonnement IPTV Maroc HD/4K — chaînes, films et séries. Test 24h gratuit. Garantie 45 jours.",
      "brand": {"@type": "Brand", "name": "Yasto.ma"},
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5",
        "reviewCount": "834",
        "bestRating": "5",
        "worstRating": "1"
      },
      "offers": [
        {"@type": "Offer", "name": "Pro", "price": "250", "priceCurrency": "MAD", "availability": "https://schema.org/InStock"},
        {"@type": "Offer", "name": "Pro+", "price": "350", "priceCurrency": "MAD", "availability": "https://schema.org/InStock"},
        {"@type": "Offer", "name": "Pro Premium", "price": "450", "priceCurrency": "MAD", "availability": "https://schema.org/InStock"}
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Qu'est-ce qu'un abonnement IPTV Maroc ?",
          "acceptedAnswer": {"@type": "Answer", "text": "Un abonnement IPTV Maroc donne accès à des chaînes TV live, films et séries via Internet, en HD ou 4K, sur Smart TV, smartphone, Fire Stick et plus."}
        },
        {
          "@type": "Question",
          "name": "Puis-je tester avant d'acheter IPTV Maroc ?",
          "acceptedAnswer": {"@type": "Answer", "text": "Oui. Yasto.ma offre un test IPTV Maroc gratuit de 24 heures via WhatsApp avant tout achat."}
        },
        {
          "@type": "Question",
          "name": "La garantie de remboursement est-elle réelle ?",
          "acceptedAnswer": {"@type": "Answer", "text": "Oui. Nos abonnements IPTV Maroc sont sous garantie 45 jours satisfait ou remboursé totalement."}
        }
      ]
    }
  ]
}
</script>
"""

# ═══════════════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════════════

home_body = f"""
<main>
  <section class="hero">
    <div class="hero-media" aria-hidden="true"></div>
    <div class="container hero-grid">
      <div class="hero-copy">
        <p class="hero-kicker">Le futur du divertissement · Maroc</p>
        <h1>Le Meilleur IPTV Maroc en 2026 : Streaming Premium Stable</h1>
        <p class="hero-sub">Meilleur abonnement 4K premium · 2026</p>
        <p class="hero-lead">Trois forfaits Yasto.ma : live, sport, VOD et essai 24h via WhatsApp.</p>
        <ul class="hero-pills">
          <li><i class="pi pi-rocket"></i> 45 000+ chaînes</li>
          <li><i class="pi pi-film"></i> Films &amp; séries</li>
          <li><i class="pi pi-hd"></i> 4K Ultra HD</li>
          <li><i class="pi pi-bolt"></i> Sans buffering</li>
        </ul>
        <div class="hero-actions">
          <a class="btn btn-whatsapp" href="{WA}?text=Bonjour%20Yasto.ma%20%F0%9F%91%8B%0AJe%20souhaite%20un%20*test%20IPTV%20Maroc%20gratuit%2024h*." target="_blank" rel="noopener noreferrer">Essai 24h gratuit</a>
          <a class="btn btn-primary" href="{WA}?text=Bonjour%20Yasto.ma%20%F0%9F%91%8B%0AJe%20veux%20*commencer*%20et%20choisir%20mon%20abonnement%20IPTV%20Maroc." target="_blank" rel="noopener noreferrer">Commencer</a>
          <a class="btn btn-ghost" href="#tarifs">Voir les forfaits</a>
        </div>
        <p class="hero-meta">Garantie 45 jours · Support 24/7 · Dès 250 DH</p>
        <p class="hero-hint">Essai 24h : test gratuit — Commencer : aide pour choisir votre forfait</p>
      </div>
      <div class="hero-visual" aria-hidden="true">
        <div class="hero-tv">
          <div class="hero-tv-screen">
            <div class="hero-tv-brand">Yasto<span>.ma</span></div>
            <div class="hero-tv-sport"></div>
            <div class="hero-tv-caption">SPORT · LIVE 4K</div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <div class="crystal-line"></div>

  <section class="section" id="avantages">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Pourquoi Yasto.ma</span>
        <h2>Pourquoi choisir notre abonnement IPTV Maroc</h2>
        <p>Nous combinons catalogue massif, serveurs OTT/VPS et accompagnement humain pour un IPTV HD Maroc et IPTV 4K Maroc réellement utilisable au quotidien.</p>
      </div>
      <div class="adv-grid">
        <article class="adv-item">
          <div class="adv-icon" aria-hidden="true">◈</div>
          <h3>Serveurs ultra-stables</h3>
          <p>Infrastructure OTT et VPS pensée pour le Maroc : moins de buffering, lecture fluide même aux heures de match.</p>
        </article>
        <article class="adv-item">
          <div class="adv-icon" aria-hidden="true">▣</div>
          <h3>Catalogue immense</h3>
          <p>Jusqu'à +45 000 chaînes et +180 000 films &amp; séries : sport, cinéma, jeunesse, chaînes marocaines, françaises et espagnoles.</p>
        </article>
        <article class="adv-item">
          <div class="adv-icon" aria-hidden="true">✦</div>
          <h3>HD &amp; 4K UHD</h3>
          <p>Du IPTV HD Maroc au IPTV 4K Maroc selon le pack. Anti-freeze 2.0 / 2.2 pour une image nette.</p>
        </article>
        <article class="adv-item">
          <div class="adv-icon" aria-hidden="true">⚙</div>
          <h3>Compatibilité totale</h3>
          <p>Smart TV, Android TV, Google TV, Fire Stick, MAG, smartphones, tablettes, PC/Mac — guide d'installation inclus.</p>
        </article>
        <article class="adv-item">
          <div class="adv-icon" aria-hidden="true">◎</div>
          <h3>Activation &amp; recharge</h3>
          <p>Activation rapide + recharge IPTV Maroc en un message WhatsApp. Multi-appareils selon le pack (1, 2 ou 3).</p>
        </article>
        <article class="adv-item">
          <div class="adv-icon" aria-hidden="true">♡</div>
          <h3>Garantie 45 jours</h3>
          <p>Satisfait ou remboursé totalement pendant 45 jours. Le risque zéro pour acheter IPTV Maroc chez un vrai fournisseur.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="container">
      <div class="counters" role="group" aria-label="Statistiques Yasto.ma">
        <div class="counter"><div class="num" data-count="12450" data-suffix="+">0</div><div class="label">Clients abonnés</div></div>
        <div class="counter"><div class="num" data-count="3180" data-suffix="">0</div><div class="label">Clients en ligne</div></div>
        <div class="counter"><div class="num" data-count="95" data-suffix="%">0</div><div class="label">Clients réabonnés</div></div>
        <div class="counter"><div class="num" data-count="834" data-suffix="">0</div><div class="label">Avis 5 étoiles</div></div>
      </div>
    </div>
  </section>

  <section class="section" id="qui-sommes-nous">
    <div class="container about-grid">
      <div class="about-copy">
        <div class="section-head">
          <span class="eyebrow">Qui sommes-nous</span>
          <h2>Yasto.ma, fournisseur IPTV Maroc orienté performance</h2>
        </div>
        <p>Yasto.ma est spécialisé dans l'<strong>abonnement IPTV Maroc</strong> haute qualité : diffusion stable, support francophone, activation sécurisée. Nous adressons les foyers au Maroc et les Marocains de France et d'Espagne qui veulent leurs chaînes nationales + le meilleur du divertissement international.</p>
        <p>Notre mission : proposer le <strong>meilleur IPTV Maroc</strong> sans promesses irréalistes — tests gratuits, packs clairs (Pro, Pro+, Pro Premium), et une vraie garantie de remboursement 45 jours.</p>
        <p>Que vous soyez à Casablanca, Marrakech, Tanger, Agadir, Rabat ou Fès, <strong>acheter IPTV Maroc</strong> chez Yasto.ma signifie un service digital immédiat, une <strong>recharge IPTV Maroc</strong> simple, et une équipe joignable sur WhatsApp {PHONE_DISPLAY}.</p>
      </div>
      <aside class="about-panel">
        <h3 style="font-family:var(--font-display);margin-bottom:0.75rem">Ce qui nous différencie</h3>
        <ul class="price-features">
          <li>Focus qualité serveur (OTT / VPS)</li>
          <li>Tests 24h avant engagement</li>
          <li>Support 24/7 (FR / Darija)</li>
          <li>Packs 1 à 3 appareils</li>
          <li>SEO &amp; service pensés pour le marché local</li>
        </ul>
        <div class="guarantee-badge">✓ Garantie 45 jours · remboursement total</div>
      </aside>
    </div>
  </section>

  {PRICING}
  {REVIEWS}
  {FORM_TEST}
  {CITIES}

  <section class="section" style="padding-top:0">
    <div class="container" style="text-align:center">
      <div class="section-head center">
        <span class="eyebrow">Ressources</span>
        <h2>Guides &amp; FAQ IPTV Maroc</h2>
        <p>Installez votre abonnement en quelques minutes et trouvez les réponses aux questions fréquentes.</p>
      </div>
      <div class="hero-actions" style="justify-content:center">
        <a class="btn btn-primary" href="/guide-installation">Guide d'installation</a>
        <a class="btn btn-ghost" href="/faq">FAQ</a>
        <a class="btn btn-ghost" href="/blog">Blog SEO</a>
      </div>
    </div>
  </section>
</main>
"""

page(
    "IPTV Maroc | Yasto.ma — Abonnement IPTV HD & 4K · Test 24h gratuit",
    "Yasto.ma : fournisseur IPTV Maroc premium. Abonnement IPTV HD/4K, +45 000 chaînes, test gratuit 24h, garantie 45 jours. Casablanca, Marrakech, Rabat, Tanger, Agadir, Fès.",
    "index.html",
    "accueil",
    home_body,
    extra=SCHEMA_HOME,
)

# Abonnement
abo_body = f"""
<main>
  <div class="container page-hero">
    <span class="eyebrow">Produit</span>
    <h1>Abonnement IPTV Maroc — packs Pro, Pro+ &amp; Pro Premium</h1>
    <p>Comparez et achetez votre <strong>abonnement IPTV Maroc</strong>. Activation rapide, multi-écrans, IPTV HD Maroc et IPTV 4K Maroc selon le pack choisi. Garantie 45 jours satisfait ou remboursé.</p>
  </div>
  {PRICING}
  <section class="section" style="padding-top:0">
    <div class="container content-page">
      <h2>Comment acheter IPTV Maroc chez Yasto.ma ?</h2>
      <p>1) Choisissez votre pack · 2) Demandez un test 24h si besoin · 3) Confirmez sur WhatsApp · 4) Recevez vos identifiants et activez sur vos appareils. La <strong>recharge IPTV Maroc</strong> se fait de la même façon à chaque renouvellement.</p>
      <h2>Quel pack choisir ?</h2>
      <p><strong>Pro (250 DHS)</strong> — idéal pour un foyer mono-écran en HD. <strong>Pro+ (350 DHS)</strong> — le meilleur rapport qualité/prix (FHD, 2 appareils, VOD enrichie). <strong>Pro Premium (450 DHS)</strong> — IPTV 4K Maroc, 3 appareils, serveur OTT VPS.</p>
      <p><a class="btn btn-primary" href="/#essai-gratuit" style="margin-top:1rem">Demander un test gratuit</a></p>
    </div>
  </section>
</main>
"""
page(
    "Abonnement IPTV Maroc | Tarifs Pro, Pro+, Premium — Yasto.ma",
    "Achetez un abonnement IPTV Maroc : Pro 250 DHS, Pro+ 350 DHS, Pro Premium 450 DHS. IPTV HD & 4K, garantie 45 jours, support 24/7 WhatsApp.",
    "/abonnement-iptv",
    "abo",
    abo_body,
)

# Guide
guide_body = f"""
<main>
  <div class="container page-hero">
    <span class="eyebrow">Installation</span>
    <h1>Guide d'installation IPTV Maroc</h1>
    <p>Installez votre <strong>abonnement IPTV Maroc</strong> sur Smart TV, Android, iOS, Fire Stick et PC. Suivez les accordéons ci-dessous — support WhatsApp {PHONE_DISPLAY} si besoin.</p>
  </div>
  <section class="section">
    <div class="container" style="max-width:800px">
      <div class="accordion">
        <div class="acc-item open">
          <button class="acc-btn" type="button" aria-expanded="true">Android / Android TV / Google TV</button>
          <div class="acc-panel">
            <ol>
              <li>Installez l'application indiquée lors de l'activation (ou IPTV Smarters / TiviMate selon pack).</li>
              <li>Ouvrez l'app → Login with Xtream Codes API (ou code d'activation fourni).</li>
              <li>Saisissez URL serveur, username et password reçus par WhatsApp.</li>
              <li>Actualisez la liste des chaînes — votre IPTV Maroc est prêt.</li>
            </ol>
          </div>
        </div>
        <div class="acc-item">
          <button class="acc-btn" type="button" aria-expanded="false">Smart TV Samsung / LG</button>
          <div class="acc-panel">
            <ol>
              <li>Ouvrez le store de la TV et installez l'app compatible fournie.</li>
              <li>Sur certains modèles : installez via SmartTube / navigateur le lien d'activation PRO.</li>
              <li>Connectez-vous avec les identifiants Yasto.ma.</li>
              <li>Pour IPTV 4K Maroc, utilisez HDMI 2.0+ et une TV UHD.</li>
            </ol>
          </div>
        </div>
        <div class="acc-item">
          <button class="acc-btn" type="button" aria-expanded="false">Amazon Fire Stick / Fire TV</button>
          <div class="acc-panel">
            <ol>
              <li>Activez « Applications de sources inconnues » dans les options appareil.</li>
              <li>Installez Downloader → entrez le code / URL fourni par le support.</li>
              <li>Installez l'APK → connectez-vous → profitez de l'IPTV HD Maroc.</li>
            </ol>
          </div>
        </div>
        <div class="acc-item">
          <button class="acc-btn" type="button" aria-expanded="false">iPhone / iPad (iOS)</button>
          <div class="acc-panel">
            <ol>
              <li>Installez l'app recommandée depuis l'App Store.</li>
              <li>Ajoutez la playlist via Xtream Codes ou fichier M3U sécurisé.</li>
              <li>Gardez une connexion Wi-Fi stable pour le streaming HD.</li>
            </ol>
          </div>
        </div>
        <div class="acc-item">
          <button class="acc-btn" type="button" aria-expanded="false">Windows / Mac</button>
          <div class="acc-panel">
            <ol>
              <li>Téléchargez VLC, IPTV Smarters Desktop ou l'app PRO.</li>
              <li>Importez la playlist ou reconnectez Xtream Codes.</li>
              <li>Privilégiez le câble Ethernet pour les matchs live.</li>
            </ol>
          </div>
        </div>
        <div class="acc-item">
          <button class="acc-btn" type="button" aria-expanded="false">MAG / Formuler / boîtiers IPTV</button>
          <div class="acc-panel">
            <p>Fournissez le numéro MAC à notre support WhatsApp. Nous poussons le portail. Redémarrez le boîtier. Votre fournisseur IPTV Maroc active le profil à distance.</p>
          </div>
        </div>
        <div class="acc-item">
          <button class="acc-btn" type="button" aria-expanded="false">Problèmes fréquents (buffering)</button>
          <div class="acc-panel">
            <ul>
              <li>Changez de serveur / DNS (1.1.1.1 ou 8.8.8.8).</li>
              <li>Passez en Wi-Fi 5 GHz ou Ethernet.</li>
              <li>Réduisez la qualité si votre débit &lt; 15 Mbps pour le 4K.</li>
              <li>Contactez le support pour un lien anti-freeze alternatif.</li>
            </ul>
          </div>
        </div>
      </div>
      <p style="margin-top:2rem"><a class="btn btn-whatsapp" href="{WA}" target="_blank" rel="noopener noreferrer">Aide installation WhatsApp</a></p>
    </div>
  </section>
</main>
"""
page(
    "Guide d'installation IPTV Maroc | Smart TV, Android, Fire Stick — Yasto.ma",
    "Guide d'installation IPTV Maroc étape par étape : Android TV, Smart TV, Fire Stick, iOS, PC. Support WhatsApp Yasto.ma 24/7.",
    "/guide-installation",
    "guide",
    guide_body,
)

# FAQ
faq_items = [
    ("Qu'est-ce que l'IPTV Maroc ?", "L'IPTV (Internet Protocol Television) diffuse les chaînes et la VOD via Internet. Un abonnement IPTV Maroc permet de regarder TV live, films et séries sur vos appareils connectés, souvent en IPTV HD Maroc ou IPTV 4K Maroc."),
    ("Yasto.ma est-il un bon fournisseur IPTV Maroc ?", "Oui : serveurs OTT/VPS, catalogue large, support WhatsApp 24/7, test 24h, garantie 45 jours. Nos clients à Casablanca, Marrakech, Rabat, Tanger, Agadir et Fès notent une forte stabilité."),
    ("Comment obtenir un test gratuit ?", "Remplissez le formulaire sur la page d'accueil ou écrivez sur WhatsApp. Vous recevez un test IPTV Maroc de 24 heures pour vérifier la qualité avant d'acheter."),
    ("Quels sont les prix ?", "Pro 250 DHS, Pro+ 350 DHS, Pro Premium 450 DHS. Voir la page Abonnement IPTV pour le détail des fonctionnalités."),
    ("Puis-je utiliser plusieurs appareils ?", "Pro : 1 appareil · Pro+ : 2 · Pro Premium : 3. Respectez le nombre d'écrans de votre pack."),
    ("Comment faire une recharge IPTV Maroc ?", "Contactez WhatsApp avant expiration. Après paiement, la recharge IPTV Maroc est appliquée sur le même compte en quelques minutes."),
    ("Y a-t-il une garantie ?", "Oui — 45 jours satisfait ou remboursé totalement, sous conditions d'usage loyal (voir politique de remboursement)."),
    ("Les chaînes marocaines sont-elles incluses ?", "Oui, les bouquets populaires + chaînes FR/ES/AR et sport selon disponibilité du catalogue live."),
    ("L'offre fonctionne-t-elle hors Maroc ?", "Oui pour la diaspora (France, Espagne, etc.), sous réserve d'une connexion Internet adaptée et du respect des conditions d'utilisation."),
    ("Comment contacter le support ?", f"WhatsApp {PHONE_DISPLAY} — disponible 24/7 pour activation, recharge et dépannage."),
]
faq_html = []
for i, (q, a) in enumerate(faq_items):
    open_cls = " open" if i == 0 else ""
    exp = "true" if i == 0 else "false"
    faq_html.append(f"""<div class="acc-item{open_cls}">
      <button class="acc-btn" type="button" aria-expanded="{exp}">{q}</button>
      <div class="acc-panel"><p>{a}</p></div>
    </div>""")

faq_schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faq_items
    ],
}
import json
faq_extra = f'<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>'

faq_body = f"""
<main>
  <div class="container page-hero">
    <span class="eyebrow">Aide</span>
    <h1>FAQ — IPTV Maroc Yasto.ma</h1>
    <p>Réponses claires sur l'abonnement IPTV Maroc, les tests, la recharge, la 4K et la garantie.</p>
  </div>
  <section class="section">
    <div class="container" style="max-width:800px">
      <div class="accordion">
        {''.join(faq_html)}
      </div>
    </div>
  </section>
</main>
"""
page(
    "FAQ IPTV Maroc | Questions fréquentes — Yasto.ma",
    "FAQ IPTV Maroc : test gratuit, prix, multi-écrans, recharge, garantie 45 jours, installation. Réponses du fournisseur Yasto.ma.",
    "/faq",
    "faq",
    faq_body,
    extra=faq_extra,
)

# Contact
contact_body = f"""
<main>
  <div class="container page-hero">
    <span class="eyebrow">Contact</span>
    <h1>Contactez Yasto.ma — Support IPTV Maroc</h1>
    <p>Une question sur votre abonnement, une demande de test ou une recharge IPTV Maroc ? Écrivez-nous.</p>
  </div>
  {FORM_TEST.replace('data-type="test"', 'data-type="contact"').replace('Essai gratuit 24 heures', 'Support & commandes').replace('Demander un test IPTV Maroc gratuit', 'Formulaire de contact IPTV Maroc')}
  <section class="section" style="padding-top:0">
    <div class="container content-page">
      <h2>Coordonnées</h2>
      <p><strong>WhatsApp :</strong> <a href="{WA}" target="_blank" rel="noopener noreferrer">{PHONE_DISPLAY}</a><br>
      <strong>E-mail :</strong> <a href="mailto:contact@yasto.ma">contact@yasto.ma</a><br>
      <strong>Site :</strong> <a href="https://yasto.ma">yasto.ma</a></p>
      <p>Horaires support : 24/7 · Langues : français, darija, espagnol (support basique).</p>
    </div>
  </section>
</main>
"""
page(
    "Contact IPTV Maroc | WhatsApp +212 664-140 211 — Yasto.ma",
    "Contactez Yasto.ma pour abonnement IPTV Maroc, test 24h, recharge et support 24/7. WhatsApp +212 664-140 211.",
    "/contact",
    "contact",
    contact_body,
)


def legal_page(slug, active, title, meta, h1, sections):
    blocks = []
    for h2, paras in sections:
        blocks.append(f"<h2>{h2}</h2>")
        for p in paras:
            blocks.append(f"<p>{p}</p>")
    body = f"""
<main>
  <div class="container page-hero">
    <span class="eyebrow">Informations légales</span>
    <h1>{h1}</h1>
  </div>
  <section class="section">
    <div class="container content-page">
      {''.join(blocks)}
      <p style="margin-top:2rem;font-size:0.9rem">Dernière mise à jour : 13 juillet 2026 · Yasto.ma</p>
    </div>
  </section>
</main>
"""
    page(title, meta, slug, active, body)


legal_page(
    "/mentions-legales", "",
    "Mentions légales | Yasto.ma IPTV Maroc",
    "Mentions légales du site Yasto.ma, fournisseur d'abonnement IPTV Maroc.",
    "Mentions légales",
    [
        ("Éditeur du site", [
            "Le site yasto.ma est édité sous la marque <strong>Yasto.ma</strong>, service digital d'abonnement IPTV destiné au marché marocain et à la diaspora.",
            "Contact : contact@yasto.ma · WhatsApp : +212 664-140 211",
        ]),
        ("Hébergement", [
            "Le site est hébergé auprès d'un prestataire cloud européen/international. Pour toute demande relative à l'hébergement, contactez contact@yasto.ma.",
        ]),
        ("Propriété intellectuelle", [
            "La marque Yasto.ma, le logo, les textes et éléments graphiques du site sont protégés. Toute reproduction non autorisée est interdite.",
        ]),
        ("Responsabilité", [
            "Yasto.ma fournit un accès technique à un service de streaming. L'utilisateur est responsable de l'usage conforme aux lois applicables dans son pays de résidence et aux présentes conditions.",
        ]),
    ],
)

legal_page(
    "/conditions-utilisation", "",
    "Conditions d'utilisation | Yasto.ma",
    "Conditions générales d'utilisation du service et du site Yasto.ma IPTV Maroc.",
    "Conditions d'utilisation",
    [
        ("Objet", [
            "Les présentes conditions régissent l'accès au site yasto.ma et l'utilisation des abonnements IPTV proposés (Pro, Pro+, Pro Premium).",
        ]),
        ("Compte & activation", [
            "L'activation est personnelle. Les identifiants ne doivent pas être revendus ni partagés au-delà du nombre d'appareils inclus dans le pack.",
        ]),
        ("Paiement & durée", [
            "Les tarifs sont indiqués en dirhams marocains (DHS). La durée et les modalités exactes sont confirmées lors de la commande WhatsApp.",
        ]),
        ("Suspension", [
            "Tout usage abusif (partage massif, revente non autorisée, attaques réseau) peut entraîner la suspension sans remboursement hors garantie légitime.",
        ]),
        ("Droit applicable", [
            "Sous réserve des règles impératives, les parties privilégient une résolution amiable via WhatsApp / e-mail avant tout litige.",
        ]),
    ],
)

legal_page(
    "/politique-utilisation-acceptable", "",
    "Politique d'utilisation acceptable | Yasto.ma",
    "Politique d'utilisation acceptable (AUP) du service IPTV Maroc Yasto.ma.",
    "Politique d'utilisation acceptable",
    [
        ("Usages autorisés", [
            "Usage privé et familial dans la limite des appareils souscrits. Consultation des contenus mis à disposition via le service souscrit.",
        ]),
        ("Usages interdits", [
            "Reselling non autorisé, partage public des identifiants, redistribution de flux, tentative d'intrusion, usage commercial non contracté.",
        ]),
        ("Débit & réseau", [
            "La qualité IPTV HD / 4K dépend de votre connexion. Nous recommandons 15–25 Mbps stables pour le FHD et 25 Mbps+ pour le 4K.",
        ]),
        ("Sanctions", [
            "En cas de non-respect, Yasto.ma peut limiter, suspendre ou résilier l'accès après notification lorsque possible.",
        ]),
    ],
)

legal_page(
    "/politique-confidentialite", "",
    "Politique de confidentialité | Yasto.ma",
    "Politique de confidentialité Yasto.ma : données collectées via formulaires et WhatsApp pour IPTV Maroc.",
    "Politique de confidentialité",
    [
        ("Données collectées", [
            "Nom, prénom, numéro de téléphone, préférences d'abonnement, échanges WhatsApp/e-mail nécessaires au service.",
        ]),
        ("Finalités", [
            "Traitement des demandes de test, activation, support, recharge IPTV Maroc, suivi commercial légitime et amélioration du service.",
        ]),
        ("Base légale", [
            "Exécution précontractuelle / contractuelle, intérêt légitime (sécurité, prévention fraude) et consentement le cas échéant.",
        ]),
        ("Conservation", [
            "Les données sont conservées le temps nécessaire à la relation commerciale et aux obligations légales, puis supprimées ou anonymisées.",
        ]),
        ("Vos droits", [
            "Accès, rectification, effacement, limitation, opposition : contactez contact@yasto.ma ou WhatsApp +212 664-140 211.",
        ]),
    ],
)

legal_page(
    "/rgpd", "",
    "Conformité RGPD | Yasto.ma",
    "Engagements de conformité RGPD / protection des données de Yasto.ma.",
    "Conformité RGPD",
    [
        ("Engagement", [
            "Yasto.ma s'aligne sur les principes du RGPD pour les personnes concernées situées dans l'EEE : minimisation, sécurité, transparence, droits des personnes.",
        ]),
        ("Mesures de sécurité", [
            "Accès limité aux données de support, échanges sur canaux contrôlés (WhatsApp Business / e-mail), sensibilisation anti-phishing.",
        ]),
        ("Sous-traitants", [
            "Hébergeur web, outils de messagerie et analytics éventuels — listés sur demande à contact@yasto.ma.",
        ]),
        ("Transferts", [
            "Si des transferts hors EEE ont lieu, des garanties appropriées sont recherchées (clauses types, etc.).",
        ]),
        ("Contact DPO / privacy", [
            "Pour toute demande RGPD : contact@yasto.ma — objet « RGPD ».",
        ]),
    ],
)

legal_page(
    "/dmca", "",
    "Politique DMCA | Yasto.ma",
    "Politique DMCA et signalement de contenus de Yasto.ma.",
    "Politique DMCA",
    [
        ("Respect des droits", [
            "Yasto.ma respecte les droits de propriété intellectuelle. Les notifications de retrait concernant des contenus allégués illicites peuvent être adressées à contact@yasto.ma.",
        ]),
        ("Contenu d'une notification", [
            "Identification de l'œuvre, localisation URL / description, coordonnées du notifiant, déclaration de bonne foi et signature.",
        ]),
        ("Traitement", [
            "Après examen, des mesures proportionnées peuvent être prises (retrait, désactivation de lien, information du client le cas échéant).",
        ]),
        ("Contre-notification", [
            "Le destinataire d'une mesure peut répondre par écrit s'il estime la notification abusive ou erronée.",
        ]),
    ],
)

legal_page(
    "/remboursement", "",
    "Remboursement et retour | Yasto.ma IPTV Maroc",
    "Politique de remboursement 45 jours satisfait ou remboursé — abonnement IPTV Maroc Yasto.ma.",
    "Remboursement et retour",
    [
        ("Garantie 45 jours", [
            "Tous nos abonnements IPTV Maroc bénéficient d'une garantie <strong>45 jours satisfait ou remboursé totalement</strong>, sous réserve d'un usage conforme.",
        ]),
        ("Conditions", [
            "Demande via WhatsApp ou e-mail avec preuve d'achat. Le compte ne doit pas avoir fait l'objet d'abus (partage excessif, revente). Un diagnostic support peut être requis (changement DNS, test débit).",
        ]),
        ("Exclusions", [
            "Problèmes liés uniquement à une connexion Internet insuffisante après conseils support ; non-respect de l'AUP ; demande hors délai de 45 jours.",
        ]),
        ("Délai de remboursement", [
            "Une fois validé, le remboursement est traité sous 3 à 10 jours ouvrés selon le moyen de paiement initial.",
        ]),
        ("Service digital", [
            "Il s'agit d'un service immatériel : pas de retour physique. La résiliation après remboursement entraîne la coupure immédiate de l'accès.",
        ]),
    ],
)

# Plan du site + sitemap html
sitemap_links = [
    ("/", "Accueil — IPTV Maroc"),
    ("/abonnement-iptv", "Abonnement IPTV"),
    ("/guide-installation", "Guide d'installation"),
    ("/faq", "FAQ"),
    ("/blog", "Blog"),
    ("/blog/meilleur-iptv-maroc-2026", "Meilleur IPTV Maroc 2026"),
    ("/blog/acheter-iptv-maroc-guide", "Acheter IPTV Maroc — guide"),
    ("/blog/iptv-4k-maroc", "IPTV 4K Maroc"),
    ("/contact", "Contact"),
    ("/mentions-legales", "Mentions légales"),
    ("/conditions-utilisation", "Conditions d'utilisation"),
    ("/politique-utilisation-acceptable", "Utilisation acceptable"),
    ("/politique-confidentialite", "Confidentialité"),
    ("/rgpd", "RGPD"),
    ("/dmca", "DMCA"),
    ("/remboursement", "Remboursement"),
    ("/plan-du-site", "Plan du site"),
    ("/sitemap", "Sitemap HTML"),
]
links_html = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in sitemap_links)

plan_body = f"""
<main>
  <div class="container page-hero">
    <span class="eyebrow">Navigation</span>
    <h1>Plan du site Yasto.ma</h1>
    <p>Retrouvez toutes les pages du site IPTV Maroc Yasto.ma.</p>
  </div>
  <section class="section">
    <div class="container">
      <ul class="sitemap-list">{links_html}</ul>
    </div>
  </section>
</main>
"""
page("Plan du site | Yasto.ma IPTV Maroc", "Plan du site Yasto.ma — toutes les pages IPTV Maroc, blog, FAQ et pages légales.", "/plan-du-site", "", plan_body)

sitemap_html_body = f"""
<main>
  <div class="container page-hero">
    <span class="eyebrow">SEO</span>
    <h1>Sitemap HTML — Yasto.ma</h1>
    <p>Index HTML des URLs publiques pour les utilisateurs et les moteurs de recherche. Voir aussi <a href="sitemap.xml">sitemap.xml</a>.</p>
  </div>
  <section class="section">
    <div class="container">
      <ul class="sitemap-list">{links_html}</ul>
    </div>
  </section>
</main>
"""
page("Sitemap HTML | Yasto.ma", "Sitemap HTML Yasto.ma — index des pages IPTV Maroc pour SEO et navigation.", "/sitemap", "", sitemap_html_body)

# Blog index + articles
articles = [
    {
        "slug": "meilleur-iptv-maroc-2026",
        "title": "Meilleur IPTV Maroc 2026 : comment bien choisir ?",
        "meta": "Guide pour trouver le meilleur IPTV Maroc en 2026 : serveurs, 4K, test gratuit, garantie. Comparatif critères Yasto.ma.",
        "excerpt": "Critères concrets pour sélectionner un fournisseur IPTV Maroc fiable cette année.",
        "body": f"""
<p>Chercher le <strong>meilleur IPTV Maroc</strong> ne se limite pas au prix le plus bas. En 2026, la qualité dépend des serveurs (OTT / VPS), de l'anti-freeze, du support et de la possibilité de tester avant d'acheter.</p>
<h2>1. Stabilité avant tout</h2>
<p>Un bon <strong>fournisseur IPTV Maroc</strong> investit dans des serveurs capables d'absorber les pics (clasicos, CAN, Ramadan). Yasto.ma propose des packs Pro+ et Pro Premium sur infrastructure OTT / OTT VPS.</p>
<h2>2. Testez 24 heures</h2>
<p>Avant d'<strong>acheter IPTV Maroc</strong>, exigez un essai. Notre test gratuit 24h sur WhatsApp permet de valider chaînes locales, sport et VOD.</p>
<h2>3. HD vs 4K</h2>
<p>L'<strong>IPTV HD Maroc</strong> suffit souvent en ADSL. L'<strong>IPTV 4K Maroc</strong> demande 25 Mbps+ et une TV UHD. Le pack Pro Premium de Yasto.ma cible ce besoin.</p>
<h2>4. Garantie &amp; recharge</h2>
<p>Privilégiez une <strong>garantie 45 jours</strong> et une <strong>recharge IPTV Maroc</strong> simple. C'est le signe d'un service conçu pour la fidélisation (chez nous ~95 % de réabonnement).</p>
<p><a class="btn btn-primary" href="/abonnement-iptv">Voir les tarifs</a> <a class="btn btn-ghost" href="/#essai-gratuit">Test gratuit</a></p>
""",
    },
    {
        "slug": "acheter-iptv-maroc-guide",
        "title": "Acheter IPTV Maroc : le guide complet (prix, packs, activation)",
        "meta": "Comment acheter IPTV Maroc en toute sécurité : packs 250 à 450 DHS, activation WhatsApp, multi-appareils, garantie.",
        "excerpt": "De la demande de test jusqu'à l'activation : le parcours d'achat Yasto.ma.",
        "body": f"""
<p><strong>Acheter IPTV Maroc</strong> doit être simple, transparent et réversible. Voici le parcours recommandé sur Yasto.ma.</p>
<h2>Étape 1 — Clarifier vos besoins</h2>
<p>1 écran HD → Pro (250 DHS). Famille 2 écrans FHD → Pro+ (350 DHS). Home cinéma 4K / 3 écrans → Pro Premium (450 DHS).</p>
<h2>Étape 2 — Test gratuit</h2>
<p>Demandez un <strong>abonnement IPTV Maroc</strong> à l'essai (24h). Vérifiez football, chaînes MA/FR/ES et la VOD.</p>
<h2>Étape 3 — Paiement &amp; activation</h2>
<p>Confirmez sur WhatsApp {PHONE_DISPLAY}. Activation en minutes. Installation via notre <a href="/guide-installation">guide</a>.</p>
<h2>Étape 4 — Recharge</h2>
<p>La <strong>recharge IPTV Maroc</strong> se fait sur le même fil WhatsApp avant expiration — sans perdre vos favoris.</p>
<p><a class="btn btn-primary" href="/contact">Commander via contact</a></p>
""",
    },
    {
        "slug": "iptv-4k-maroc",
        "title": "IPTV 4K Maroc : débit, TV et pack Premium",
        "meta": "Tout savoir sur l'IPTV 4K Maroc : débit Internet, Anti-freeze 2.2, pack Pro Premium Yasto.ma 450 DHS.",
        "excerpt": "Les conditions techniques pour profiter vraiment de l'UHD au Maroc.",
        "body": """
<p>L'<strong>IPTV 4K Maroc</strong> offre une image Ultra HD lorsque votre réseau et votre écran suivent. Sans cela, mieux vaut rester en <strong>IPTV HD Maroc</strong> fluide.</p>
<h2>Débit recommandé</h2>
<p>25 à 50 Mbps stables, idéalement en fibre ou 5 GHz. Évitez le partage excessif du Wi-Fi pendant les matchs.</p>
<h2>Matériel</h2>
<p>TV 4K + HDMI 2.0 / boîtier récent (Fire Stick 4K, Android TV). Le pack <strong>Pro Premium</strong> Yasto.ma active la résolution 4K UHD et Anti-freeze 2.2 sur serveur OTT VPS.</p>
<h2>Villes couvertes</h2>
<p>Service digital pour Casablanca, Marrakech, Rabat, Tanger, Agadir, Fès et partout où Internet le permet — y compris diaspora FR/ES.</p>
<p><a class="btn btn-primary" href="/abonnement-iptv">Pack Pro Premium</a></p>
""",
    },
]

blog_cards = []
for a in articles:
    blog_cards.append(f"""
    <article class="blog-card">
      <div class="thumb" role="presentation"></div>
      <div class="body">
        <h3><a href="/blog/{a['slug']}">{a['title']}</a></h3>
        <p>{a['excerpt']}</p>
        <div class="blog-meta">IPTV Maroc · Lecture 4 min</div>
      </div>
    </article>""")

blog_index = f"""
<main>
  <div class="container page-hero">
    <span class="eyebrow">Blog SEO</span>
    <h1>Blog IPTV Maroc — guides &amp; conseils Yasto.ma</h1>
    <p>Articles optimisés autour de <strong>IPTV Maroc</strong>, abonnement, 4K, recharge et choix du meilleur fournisseur.</p>
  </div>
  <section class="section">
    <div class="container">
      <div class="blog-grid">{''.join(blog_cards)}</div>
    </div>
  </section>
</main>
"""
page(
    "Blog IPTV Maroc | Guides SEO — Yasto.ma",
    "Blog Yasto.ma : guides pour choisir, acheter et installer un abonnement IPTV Maroc HD/4K.",
    "/blog",
    "blog",
    blog_index,
    depth=1,
)

for a in articles:
    art_body = f"""
<main>
  <div class="container page-hero">
    <span class="eyebrow"><a href="/blog">Blog</a></span>
    <h1>{a['title']}</h1>
    <p>{a['excerpt']}</p>
  </div>
  <section class="section">
    <div class="container content-page">
      {a['body']}
    </div>
  </section>
</main>
"""
    page(a["title"] + " | Yasto.ma", a["meta"], f"blog/{a['slug']}", "blog", art_body, depth=1, og_type="article")

# robots.txt + sitemap.xml
urls = [
    ("/", "1.0", "daily"),
    ("/abonnement-iptv", "0.9", "weekly"),
    ("/guide-installation", "0.8", "monthly"),
    ("/faq", "0.8", "monthly"),
    ("/contact", "0.7", "monthly"),
    ("/blog", "0.8", "weekly"),
    ("/blog/meilleur-iptv-maroc-2026", "0.7", "monthly"),
    ("/blog/acheter-iptv-maroc-guide", "0.7", "monthly"),
    ("/blog/iptv-4k-maroc", "0.7", "monthly"),
    ("/mentions-legales", "0.3", "yearly"),
    ("/conditions-utilisation", "0.3", "yearly"),
    ("/politique-confidentialite", "0.4", "yearly"),
    ("/politique-utilisation-acceptable", "0.3", "yearly"),
    ("/rgpd", "0.3", "yearly"),
    ("/dmca", "0.3", "yearly"),
    ("/remboursement", "0.5", "yearly"),
    ("/plan-du-site", "0.4", "monthly"),
    ("/sitemap", "0.4", "monthly"),
]
xml_items = []
for u, prio, freq in urls:
    loc = canonical_url(u)
    xml_items.append(f"""  <url>
    <loc>{loc}</loc>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>""")
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(xml_items)
    + "\n</urlset>\n",
    encoding="utf-8",
)
(ROOT / "robots.txt").write_text(
    f"""User-agent: *
Allow: /

Sitemap: {SITE}/sitemap.xml
""",
    encoding="utf-8",
)
print("Wrote sitemap.xml, robots.txt")
print("Done.")
