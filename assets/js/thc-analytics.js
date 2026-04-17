/*
 * Tracy Harris Co — Analytics layer (PostHog Cloud EU)
 * ----------------------------------------------------
 * This file:
 *   1. Loads PostHog from the EU region with our project API key
 *   2. Auto-registers recipe_id from the document body as a session super-property
 *   3. Exposes convenience helpers for the events we actually care about
 *
 * Public API (on window.thc):
 *   thc.trackApplyClick(product)          // 'ffb' | 'ffm' | 'elite' | 'fresh-reset'
 *   thc.trackOptinSubmit(form, meta?)     // e.g. 'fresh-quiz', 'newsletter'
 *   thc.trackWorkshopRegister(slug)       // e.g. 'million-dollar-message'
 *   thc.trackCustom(eventName, props?)    // anything else, bring your own props
 *   thc.identify(userId, traits?)         // after form submit: stitch sessions to a real person
 *
 * The recipe_id on <body data-recipe-id="rcp_..."> is read automatically at page load.
 *
 * Drop this single tag in <head> AFTER the posthog snippet below fires:
 *   <script src="https://purepurposekh.github.io/tracy-harris-brand-kit/assets/js/thc-analytics.js"></script>
 *
 * Or inline the whole thing into your site's header if you want zero network hops.
 */

(function () {
  'use strict';

  var POSTHOG_KEY = 'phc_yvn2WdBhF8fZYpQExJbXpJg7Y6ivVbpy7uect6zgWgK8';
  var POSTHOG_HOST = 'https://eu.i.posthog.com';

  // Official PostHog JS snippet (trimmed to essentials; full flags/replay are tree-shaken at load time).
  // Reference: https://posthog.com/docs/libraries/js#option-1-add-the-javascript-snippet-to-your-html
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init Ie _calculate_event_properties Js register register_once register_for_session unregister unregister_for_session Rs getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSurveysLoaded onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey canRenderSurveyAsync identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty Ds Fs createPersonProfile Ls Ps opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing Cs debug I As getPageViewId captureTraceFeedback captureTraceMetric".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

  // Initialise PostHog immediately
  posthog.init(POSTHOG_KEY, {
    api_host: POSTHOG_HOST,
    person_profiles: 'identified_only',        // only create profiles when we identify(), keeps billing lean
    capture_pageview: true,                    // auto $pageview on load + SPA navigation
    capture_pageleave: true,                   // $pageleave for accurate time-on-page
    autocapture: true,                         // clicks / form submits auto-tagged (set false if you want manual only)
    disable_session_recording: false,          // we want replay; mask PII via HTML attributes (see masking section below)
    session_recording: {
      maskAllInputs: true,                     // hard mask ALL form inputs — never leak Apply/Opt-in submissions
      maskInputOptions: { password: true, email: true }
    },
    persistence: 'localStorage+cookie',
    respect_dnt: true,                         // honour Do Not Track
    loaded: function (ph) {
      // Auto-read recipe_id from <body data-recipe-id="...">
      try {
        var rid = document.body && document.body.getAttribute('data-recipe-id');
        if (rid) {
          ph.register({ recipe_id: rid });
        }
      } catch (e) { /* no-op */ }
    }
  });

  // --------- Convenience helpers ---------

  function safeCapture(event, props) {
    try {
      if (window.posthog && typeof posthog.capture === 'function') {
        posthog.capture(event, props || {});
      }
    } catch (e) {
      // silent — analytics must never break page UX
    }
  }

  var thc = {
    version: '1.0.0',
    ph: function () { return window.posthog; },

    trackApplyClick: function (product) {
      safeCapture('apply_click', { product: String(product || '').toLowerCase() });
    },

    trackOptinSubmit: function (form, meta) {
      safeCapture('optin_submit', Object.assign({ form: String(form || '').toLowerCase() }, meta || {}));
    },

    trackWorkshopRegister: function (slug) {
      safeCapture('workshop_register', { workshop: String(slug || '').toLowerCase() });
    },

    trackCustom: function (name, props) {
      if (!name) return;
      safeCapture(name, props || {});
    },

    identify: function (userId, traits) {
      try {
        if (window.posthog && typeof posthog.identify === 'function' && userId) {
          posthog.identify(String(userId), traits || {});
        }
      } catch (e) { /* no-op */ }
    },

    // Call from form onsubmit if you want to both track + identify in one line
    trackAndIdentifyFromForm: function (formId, emailFieldName) {
      try {
        var form = document.getElementById(formId);
        if (!form) return;
        var email = form.elements[emailFieldName || 'email'] && form.elements[emailFieldName || 'email'].value;
        if (email) {
          thc.identify(email, { email: email });
          thc.trackOptinSubmit(formId);
        }
      } catch (e) { /* no-op */ }
    }
  };

  // Auto-wire common CTAs via data attributes. Drop data-track="apply" on any Apply link, etc.
  function wireDataTracking() {
    try {
      document.querySelectorAll('[data-track]').forEach(function (el) {
        el.addEventListener('click', function () {
          var kind = el.getAttribute('data-track');
          var product = el.getAttribute('data-product') || '';
          if (kind === 'apply') thc.trackApplyClick(product);
          else if (kind === 'workshop') thc.trackWorkshopRegister(product);
          else if (kind === 'custom') thc.trackCustom(el.getAttribute('data-event') || 'cta_click', { label: el.textContent.trim() });
        });
      });
    } catch (e) { /* no-op */ }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wireDataTracking);
  } else {
    wireDataTracking();
  }

  window.thc = thc;
})();
