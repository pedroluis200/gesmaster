var Vuelidate=function(e,t){"use strict";function r(e){let r=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[];return Object.keys(e).reduce((n,a)=>(r.includes(a)||(n[a]=t.unref(e[a])),n),{})}function n(e){return"function"==typeof e}function a(e){return t.isReactive(e)||t.isReadonly(e)}function u(e,t,r){let n=e;const a=t.split(".");for(let e=0;e<a.length;e++){if(!n[a[e]])return r;n=n[a[e]]}return n}function l(e,r,n){return t.computed(()=>e.some(e=>u(r,e,{[n]:!1})[n]))}function s(e,r,n){return t.computed(()=>e.reduce((e,t)=>{const a=u(r,t,{[n]:!1})[n]||[];return e.concat(a)},[]))}function o(e,r,n,a){return e.call(a,t.unref(r),t.unref(n),a)}function i(e){return void 0!==e.$valid?!e.$valid:!e}function c(e,a,u,l,s,c,$,v,d,f,p){const h=t.ref(!1),m=e.$params||{},g=t.ref(null);let y,R;e.$async?({$invalid:y,$unwatch:R}=function(e,r,n,a,u,l,s){let{$lazy:c,$rewardEarly:$}=u,v=arguments.length>7&&void 0!==arguments[7]?arguments[7]:[],d=arguments.length>8?arguments[8]:void 0,f=arguments.length>9?arguments[9]:void 0,p=arguments.length>10?arguments[10]:void 0;const h=t.ref(!!a.value),m=t.ref(0);n.value=!1;const g=t.watch([r,a].concat(v,p),()=>{if(c&&!a.value||$&&!f.value&&!n.value)return;let t;try{t=o(e,r,d,s)}catch(e){t=Promise.reject(e)}m.value++,n.value=!!m.value,h.value=!1,Promise.resolve(t).then(e=>{m.value--,n.value=!!m.value,l.value=e,h.value=i(e)}).catch(e=>{m.value--,n.value=!!m.value,l.value=e,h.value=!0})},{immediate:!0,deep:"object"==typeof r});return{$invalid:h,$unwatch:g}}(e.$validator,a,h,u,l,g,s,e.$watchTargets,d,f,p)):({$invalid:y,$unwatch:R}=function(e,r,n,a,u,l,s,c){let{$lazy:$,$rewardEarly:v}=a;return{$unwatch:()=>({}),$invalid:t.computed(()=>{if($&&!n.value||v&&!c.value)return!1;let t=!0;try{const n=o(e,r,s,l);u.value=n,t=i(n)}catch(e){u.value=e}return t})}}(e.$validator,a,u,l,g,s,d,f));const E=e.$message;return{$message:n(E)?t.computed(()=>E(r({$pending:h,$invalid:y,$params:r(m),$model:a,$response:g,$validator:c,$propertyPath:v,$property:$}))):E||"",$params:m,$pending:h,$invalid:y,$response:g,$unwatch:R}}function $(){}function v(e,t,r){if(r)return t?t(e()):e();try{var n=Promise.resolve(e());return t?n.then(t):n}catch(e){return Promise.reject(e)}}function d(e){const r=(a=function(){return F(),function(e,t){var r=e();return r&&r.then?r.then(t):t(r)}((function(){if(C.$rewardEarly)return z(),v(t.nextTick,$,e);var e}),(function(){return v(t.nextTick,(function(){return new Promise(e=>{if(!N.value)return e(!T.value);const r=t.watch(N,()=>{e(!T.value),r()})})}))}))},function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];try{return Promise.resolve(a.apply(this,e))}catch(e){return Promise.reject(e)}});var a;let{validations:u,state:o,key:i,parentKey:f,childResults:p,resultsCache:h,globalConfig:m={},instance:g,externalResults:y}=e;const R=f?`${f}.${i}`:i,{rules:E,nestedValidators:b,config:j,validationGroups:w}=function(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};const r=t.unref(e),a=Object.keys(r),u={},l={},s={};let o=null;return a.forEach(e=>{const t=r[e];switch(!0){case n(t.$validator):u[e]=t;break;case n(t):u[e]={$validator:t};break;case"$validationGroups"===e:o=t;break;case e.startsWith("$"):s[e]=t;break;default:l[e]=t}}),{rules:u,nestedValidators:l,config:s,validationGroups:o}}(u),C=Object.assign({},m,j),O=i?t.computed(()=>{const e=t.unref(o);return e?t.unref(e[i]):void 0}):o,_=Object.assign({},t.unref(y)||{}),k=t.computed(()=>{const e=t.unref(y);return i?e?t.unref(e[i]):void 0:e}),P=function(e,r,n,a,u,l,s,o,i){const $=Object.keys(e),v=a.get(u,e),d=t.ref(!1),f=t.ref(!1),p=t.ref(0);if(v){if(!v.$partial)return v;v.$unwatch(),d.value=v.$dirty.value}const h={$dirty:d,$path:u,$touch:()=>{d.value||(d.value=!0)},$reset:()=>{d.value&&(d.value=!1)},$commit:()=>{}};return $.length?($.forEach(t=>{h[t]=c(e[t],r,h.$dirty,l,s,t,n,u,i,f,p)}),h.$externalResults=t.computed(()=>o.value?[].concat(o.value).map((e,t)=>({$propertyPath:u,$property:n,$validator:"$externalResults",$uid:`${u}-externalResult-${t}`,$message:e,$params:{},$response:null,$pending:!1})):[]),h.$invalid=t.computed(()=>{const e=$.some(e=>t.unref(h[e].$invalid));return f.value=e,!!h.$externalResults.value.length||e}),h.$pending=t.computed(()=>$.some(e=>t.unref(h[e].$pending))),h.$error=t.computed(()=>!!h.$dirty.value&&(h.$pending.value||h.$invalid.value)),h.$silentErrors=t.computed(()=>$.filter(e=>t.unref(h[e].$invalid)).map(e=>{const r=h[e];return t.reactive({$propertyPath:u,$property:n,$validator:e,$uid:`${u}-${e}`,$message:r.$message,$params:r.$params,$response:r.$response,$pending:r.$pending})}).concat(h.$externalResults.value)),h.$errors=t.computed(()=>h.$dirty.value?h.$silentErrors.value:[]),h.$unwatch=()=>$.forEach(e=>{h[e].$unwatch()}),h.$commit=()=>{f.value=!0,p.value=Date.now()},a.set(u,e,h),h):(v&&a.set(u,e,h),h)}(E,O,i,h,R,C,g,k,o),L=function(e,t,r,n,a,u,l){const s=Object.keys(e);return s.length?s.reduce((s,o)=>(s[o]=d({validations:e[o],state:t,key:o,parentKey:r,resultsCache:n,globalConfig:a,instance:u,externalResults:l}),s),{}):{}}(b,O,R,h,C,g,k),x={};w&&Object.entries(w).forEach(e=>{let[t,r]=e;x[t]={$invalid:l(r,L,"$invalid"),$error:l(r,L,"$error"),$pending:l(r,L,"$pending"),$errors:s(r,L,"$errors"),$silentErrors:s(r,L,"$silentErrors")}});const{$dirty:V,$errors:I,$invalid:T,$anyDirty:D,$error:A,$pending:N,$touch:F,$reset:G,$silentErrors:M,$commit:z}=function(e,r,n){const a=t.computed(()=>[r,n].filter(e=>e).reduce((e,r)=>e.concat(Object.values(t.unref(r))),[])),u=t.computed({get:()=>e.$dirty.value||!!a.value.length&&a.value.every(e=>e.$dirty),set(t){e.$dirty.value=t}}),l=t.computed(()=>{const r=t.unref(e.$silentErrors)||[],n=a.value.filter(e=>(t.unref(e).$silentErrors||[]).length).reduce((e,t)=>e.concat(...t.$silentErrors),[]);return r.concat(n)}),s=t.computed(()=>{const r=t.unref(e.$errors)||[],n=a.value.filter(e=>(t.unref(e).$errors||[]).length).reduce((e,t)=>e.concat(...t.$errors),[]);return r.concat(n)}),o=t.computed(()=>a.value.some(e=>e.$invalid)||t.unref(e.$invalid)||!1),i=t.computed(()=>a.value.some(e=>t.unref(e.$pending))||t.unref(e.$pending)||!1),c=t.computed(()=>a.value.some(e=>e.$dirty)||a.value.some(e=>e.$anyDirty)||u.value),$=t.computed(()=>!!u.value&&(i.value||o.value)),v=()=>{e.$touch(),a.value.forEach(e=>{e.$touch()})};return a.value.length&&a.value.every(e=>e.$dirty)&&v(),{$dirty:u,$errors:s,$invalid:o,$anyDirty:c,$error:$,$pending:i,$touch:v,$reset:()=>{e.$reset(),a.value.forEach(e=>{e.$reset()})},$silentErrors:l,$commit:()=>{e.$commit(),a.value.forEach(e=>{e.$commit()})}}}(P,L,p),B=i?t.computed({get:()=>t.unref(O),set:e=>{V.value=!0;const r=t.unref(o),n=t.unref(y);n&&(n[i]=_[i]),t.isRef(r[i])?r[i].value=e:r[i]=e}}):null;return i&&C.$autoDirty&&t.watch(O,()=>{V.value||F();const e=t.unref(y);e&&(e[i]=_[i])},{flush:"sync"}),t.reactive(Object.assign({},P,{$model:B,$dirty:V,$error:A,$errors:I,$invalid:T,$anyDirty:D,$pending:N,$touch:F,$reset:G,$path:R||"__root",$silentErrors:M,$validate:r,$commit:z},p&&{$getResultsForChild:function(e){return(p.value||{})[e]},$clearExternalResults:function(){t.isRef(y)?y.value=_:0===Object.keys(_).length?Object.keys(y).forEach(e=>{delete y[e]}):Object.assign(y,_)},$validationGroups:x},L))}class f{constructor(){this.storage=new Map}set(e,t,r){this.storage.set(e,{rules:t,result:r})}checkRulesValidity(e,r,n){const a=Object.keys(n),u=Object.keys(r);if(u.length!==a.length)return!1;return!!u.every(e=>a.includes(e))&&u.every(e=>!r[e].$params||Object.keys(r[e].$params).every(a=>t.unref(n[e].$params[a])===t.unref(r[e].$params[a])))}get(e,t){const r=this.storage.get(e);if(!r)return;const{rules:n,result:a}=r,u=this.checkRulesValidity(e,t,n),l=a.$unwatch?a.$unwatch:()=>({});return u?a:{$dirty:a.$dirty,$partial:!0,$unwatch:l}}}const p={COLLECT_ALL:!0,COLLECT_NONE:!1},h=Symbol("vuelidate#injectChildResults"),m=Symbol("vuelidate#removeChildResults");function g(e){let{$scope:r,instance:n}=e;const a={},u=t.ref([]),l=t.computed(()=>u.value.reduce((e,r)=>(e[r]=t.unref(a[r]),e),{}));n.__vuelidateInjectInstances=[].concat(n.__vuelidateInjectInstances||[],(function(e,t){let{$registerAs:n,$scope:l,$stopPropagation:s}=t;s||r===p.COLLECT_NONE||l===p.COLLECT_NONE||r!==p.COLLECT_ALL&&r!==l||(a[n]=e,u.value.push(n))})),n.__vuelidateRemoveInstances=[].concat(n.__vuelidateRemoveInstances||[],(function(e){u.value=u.value.filter(t=>t!==e),delete a[e]}));const s=t.inject(h,[]);t.provide(h,n.__vuelidateInjectInstances);const o=t.inject(m,[]);return t.provide(m,n.__vuelidateRemoveInstances),{childResults:l,sendValidationResultsToParent:s,removeValidationResultsFromParent:o}}function y(e){return new Proxy(e,{get:(e,r)=>"object"==typeof e[r]?y(e[r]):t.computed(()=>e[r])})}let R=0;function E(e,r){var u;let l=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{};1===arguments.length&&(l=e,e=void 0,r=void 0);let{$registerAs:s,$scope:o=p.COLLECT_ALL,$stopPropagation:i,$externalResults:c,currentVueInstance:$}=l;const v=$||(null===(u=t.getCurrentInstance())||void 0===u?void 0:u.proxy),h=v?v.$options:{};s||(R+=1,s="_vuelidate_"+R);const m=t.ref({}),E=new f,{childResults:b,sendValidationResultsToParent:j,removeValidationResultsFromParent:w}=v?g({$scope:o,instance:v}):{childResults:t.ref({})};if(!e&&h.validations){const e=h.validations;r=t.ref({}),t.onBeforeMount(()=>{r.value=v,t.watch(()=>n(e)?e.call(r.value,new y(r.value)):e,e=>{m.value=d({validations:e,state:r,childResults:b,resultsCache:E,globalConfig:l,instance:v,externalResults:c||v.vuelidateExternalResults})},{immediate:!0})}),l=h.validationsConfig||l}else{const n=t.isRef(e)||a(e)?e:t.reactive(e||{});t.watch(n,e=>{m.value=d({validations:e,state:r,childResults:b,resultsCache:E,globalConfig:l,instance:null!=v?v:{},externalResults:c})},{immediate:!0})}return v&&(j.forEach(e=>e(m,{$registerAs:s,$scope:o,$stopPropagation:i})),t.onBeforeUnmount(()=>w.forEach(e=>e(s)))),t.computed(()=>Object.assign({},t.unref(m.value),b.value))}return e.CollectFlag=p,e.default=E,e.useVuelidate=E,Object.defineProperty(e,"__esModule",{value:!0}),e}({},VueDemi);
//# sourceMappingURL=index.iife.min.js.map