"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[232],{81788:(e,t,r)=>{r.d(t,{B8:()=>i,TZ:()=>o,mf:()=>l,u7:()=>d});var n=r(31069),a=r(68492);const s=(e,t,r)=>{let n=`api/v1/dashboard/${e}/filter_state`;return t&&(n=n.concat(`/${t}`)),r&&(n=n.concat(`?tab_id=${r}`)),n},o=(e,t,r,o)=>n.Z.put({endpoint:s(e,r,o),jsonPayload:{value:t}}).then((e=>e.json.message)).catch((e=>(a.Z.error(e),null))),d=(e,t,r)=>n.Z.post({endpoint:s(e,void 0,r),jsonPayload:{value:t}}).then((e=>e.json.key)).catch((e=>(a.Z.error(e),null))),i=(e,t)=>n.Z.get({endpoint:s(e,t)}).then((e=>{let{json:t}=e;return JSON.parse(t.value)})).catch((e=>(a.Z.error(e),null))),l=e=>n.Z.get({endpoint:`/api/v1/dashboard/permalink/${e}`}).then((e=>{let{json:t}=e;return t})).catch((e=>(a.Z.error(e),null)))},50232:(e,t,r)=>{r.r(t),r.d(t,{DashboardPage:()=>z,DashboardPageIdContext:()=>U,default:()=>M});var n=r(67294),a=r(11965),s=r(16550),o=r(51995),d=r(93185),i=r(78161),l=r(28062),c=r(55867),u=r(78718),p=r.n(u),h=r(28216),m=r(14114),b=r(38703),f=r(63043),g=r(4305),y=r(50810),v=r(14505),x=r(74298),$=r(61337),_=r(27600),E=r(23525),I=r(52794),S=r(9467),w=r(81788),R=r(14670),Z=r.n(R),T=r(43399);const j=e=>a.iv`
  body {
    h1 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.xxl}px;
      letter-spacing: -0.2px;
      margin-top: ${3*e.gridUnit}px;
      margin-bottom: ${3*e.gridUnit}px;
    }

    h2 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.xl}px;
      margin-top: ${3*e.gridUnit}px;
      margin-bottom: ${2*e.gridUnit}px;
    }

    h3,
    h4,
    h5,
    h6 {
      font-weight: ${e.typography.weights.bold};
      line-height: 1.4;
      font-size: ${e.typography.sizes.l}px;
      letter-spacing: 0.2px;
      margin-top: ${2*e.gridUnit}px;
      margin-bottom: ${e.gridUnit}px;
    }
  }
`,q=e=>a.iv`
  .filter-card-popover {
    width: 240px;
    padding: 0;
    border-radius: 4px;

    &.ant-popover-placement-bottom {
      padding-top: ${e.gridUnit}px;
    }

    &.ant-popover-placement-left {
      padding-right: ${3*e.gridUnit}px;
    }

    .ant-popover-inner {
      box-shadow: 0 0 8px rgb(0 0 0 / 10%);
    }

    .ant-popover-inner-content {
      padding: ${4*e.gridUnit}px;
    }

    .ant-popover-arrow {
      display: none;
    }
  }

  .filter-card-tooltip {
    &.ant-tooltip-placement-bottom {
      padding-top: 0;
      & .ant-tooltip-arrow {
        top: -13px;
      }
    }
  }
`,C=e=>a.iv`
  .ant-dropdown-menu.chart-context-menu {
    min-width: ${43*e.gridUnit}px;
  }
  .ant-dropdown-menu-submenu.chart-context-submenu {
    max-width: ${60*e.gridUnit}px;
    min-width: ${40*e.gridUnit}px;
  }
`,U=n.createContext("");(0,x.Z)();const k=n.lazy((()=>Promise.all([r.e(1216),r.e(527),r.e(1247),r.e(8),r.e(981),r.e(5207),r.e(5640),r.e(3197),r.e(95),r.e(868),r.e(9540),r.e(4717),r.e(452)]).then(r.bind(r,31487)))),L=document.title,F=()=>{const e=(0,$.rV)($.dR.dashboard__explore_context,{});return Object.fromEntries(Object.entries(e).filter((e=>{let[,t]=e;return!t.isRedundant})))},Q=(e,t)=>{const r=F();(0,$.LS)($.dR.dashboard__explore_context,{...r,[e]:t})},z=e=>{let{idOrSlug:t}=e;const r=(0,o.Fg)(),u=(0,h.I0)(),x=(0,s.k6)(),R=(()=>{const e=(0,n.useMemo)((()=>Z().generate()),[]),t=(0,h.v9)((t=>{var r,n,a;let{dashboardInfo:s,dashboardState:o,nativeFilters:d,dataMask:i}=t;return{labelColors:(null==(r=s.metadata)?void 0:r.label_colors)||{},sharedLabelColors:(null==(n=s.metadata)?void 0:n.shared_label_colors)||{},colorScheme:null==o?void 0:o.colorScheme,chartConfiguration:(null==(a=s.metadata)?void 0:a.chart_configuration)||{},nativeFilters:Object.entries(d.filters).reduce(((e,t)=>{let[r,n]=t;return{...e,[r]:p()(n,["chartsInScope"])}}),{}),dataMask:i,dashboardId:s.id,filterBoxFilters:(0,T.De)(),dashboardPageId:e}}));return(0,n.useEffect)((()=>(Q(e,t),()=>{Q(e,{...t,isRedundant:!0})})),[t,e]),e})(),{addDangerToast:z}=(0,m.e1)(),{result:M,error:A}=(0,f.QU)(t),{result:P,error:O}=(0,f.Es)(t),{result:D,error:N,status:B}=(0,f.JL)(t),J=(0,n.useRef)(!1),K=A||O,V=Boolean(M&&P),{dashboard_title:Y,css:H,metadata:X,id:G=0}=M||{};if((0,n.useEffect)((()=>{const e=()=>{const e=F();(0,$.LS)($.dR.dashboard__explore_context,{...e,[R]:{...e[R],isRedundant:!0}})};return window.addEventListener("beforeunload",e),()=>{window.removeEventListener("beforeunload",e)}}),[R]),(0,n.useEffect)((()=>{u((0,S.sL)(B))}),[u,B]),(0,n.useEffect)((()=>{G&&async function(){const e=(0,E.eY)(_.KD.permalinkKey),t=(0,E.eY)(_.KD.nativeFiltersKey),r=(0,E.eY)(_.KD.nativeFilters);let n,a=t||{};if(e){const t=await(0,w.mf)(e);t&&({dataMask:a,activeTabs:n}=t.state)}else t&&(a=await(0,w.B8)(G,t));r&&(a=r),V&&(J.current||(J.current=!0,(0,d.c)(d.T.DASHBOARD_NATIVE_FILTERS_SET)&&u((0,I.pi)(G))),u((0,g.Y)({history:x,dashboard:M,charts:P,activeTabs:n,dataMask:a})))}()}),[V]),(0,n.useEffect)((()=>(Y&&(document.title=Y),()=>{document.title=L})),[Y]),(0,n.useEffect)((()=>"string"==typeof H?(0,v.Z)(H):()=>{}),[H]),(0,n.useEffect)((()=>{const e=(0,i.ZP)();return e.source=i.Ag.dashboard,()=>{l.getNamespace(null==X?void 0:X.color_namespace).resetColors(),e.clear()}}),[null==X?void 0:X.color_namespace]),(0,n.useEffect)((()=>{N?z((0,c.t)("Error loading chart datasources. Filters may not work correctly.")):u((0,y.Fy)(D))}),[z,D,N,u]),K)throw K;return V&&J.current?(0,a.tZ)(n.Fragment,null,(0,a.tZ)(a.xB,{styles:[q(r),j(r),C(r),"",""]}),(0,a.tZ)(U.Provider,{value:R},(0,a.tZ)(k,null))):(0,a.tZ)(b.Z,null)},M=z},14505:(e,t,r)=>{function n(e){const t="CssEditor-css",r=document.head||document.getElementsByTagName("head")[0],n=document.querySelector(`.${t}`)||function(e){const t=document.createElement("style");return t.className="CssEditor-css",t.type="text/css",t}();return"styleSheet"in n?n.styleSheet.cssText=e:n.innerHTML=e,r.appendChild(n),function(){n.remove()}}r.d(t,{Z:()=>n})},63043:(e,t,r)=>{r.d(t,{hb:()=>d,QU:()=>i,Es:()=>l,JL:()=>c,L8:()=>w,Xx:()=>y,SJ:()=>E,uY:()=>_,zA:()=>I});var n=r(42190),a=r(15926);function s(e){let{owners:t}=e;return t?t.map((e=>`${e.first_name} ${e.last_name}`)):null}const o=r.n(a)().encode({columns:["owners.first_name","owners.last_name"],keys:["none"]});function d(e){return(0,n.l6)((0,n.s_)(`/api/v1/chart/${e}?q=${o}`),s)}const i=e=>(0,n.l6)((0,n.s_)(`/api/v1/dashboard/${e}`),(e=>({...e,metadata:e.json_metadata&&JSON.parse(e.json_metadata)||{},position_data:e.position_json&&JSON.parse(e.position_json)}))),l=e=>(0,n.s_)(`/api/v1/dashboard/${e}/charts`),c=e=>(0,n.s_)(`/api/v1/dashboard/${e}/datasets`);var u=r(67294),p=r(38325),h=r(10362);const m=h.h.injectEndpoints({endpoints:e=>({schemas:e.query({providesTags:[{type:"Schemas",id:"LIST"}],query:e=>{let{dbId:t,forceRefresh:r}=e;return{endpoint:`/api/v1/database/${t}/schemas/`,urlParams:{force:r},transformResponse:e=>{let{json:t}=e;return t.result.map((e=>({value:e,label:e,title:e})))}}},serializeQueryArgs:e=>{let{queryArgs:{dbId:t}}=e;return{dbId:t}}})})}),{useLazySchemasQuery:b,useSchemasQuery:f}=m,g=[];function y(e){const t=(0,u.useRef)(!1),{dbId:r,onSuccess:n,onError:a}=e||{},[s]=b(),o=f({dbId:r,forceRefresh:!1},{skip:!r}),d=(0,p.Z)(((e,t)=>{null==n||n(e,t)})),i=(0,p.Z)((()=>{null==a||a()})),l=(0,u.useCallback)((()=>{r&&s({dbId:r,forceRefresh:!0}).then((e=>{let{isSuccess:t,isError:r,data:n}=e;t&&d(n||g,!0),r&&i()}))}),[r,i,d,s]);return(0,u.useEffect)((()=>{if(t.current){const{requestId:e,isSuccess:t,isError:r,isFetching:n,data:a,originalArgs:s}=o;null!=s&&s.forceRefresh||!e||n||(t&&d(a||g,!1),r&&i())}else t.current=!0}),[o,d,i]),{...o,refetch:l}}const v=h.h.injectEndpoints({endpoints:e=>({tables:e.query({providesTags:["Tables"],query:e=>{let{dbId:t,schema:r,forceRefresh:n}=e;return{endpoint:`/api/v1/database/${null!=t?t:"undefined"}/tables/`,urlParams:{force:n,schema_name:r?encodeURIComponent(r):""},transformResponse:e=>{let{json:t}=e;return{options:t.result,hasMore:t.count>t.result.length}}}},serializeQueryArgs:e=>{let{queryArgs:{dbId:t,schema:r}}=e;return{dbId:t,schema:r}}}),tableMetadata:e.query({query:e=>{let{dbId:t,schema:r,table:n}=e;return{endpoint:`/api/v1/database/${t}/table/${encodeURIComponent(n)}/${encodeURIComponent(r)}/`,transformResponse:e=>{let{json:t}=e;return t}}}}),tableExtendedMetadata:e.query({query:e=>{let{dbId:t,schema:r,table:n}=e;return{endpoint:`/api/v1/database/${t}/table_extra/${encodeURIComponent(n)}/${encodeURIComponent(r)}/`,transformResponse:e=>{let{json:t}=e;return t}}}})})}),{useLazyTablesQuery:x,useTablesQuery:$,useTableMetadataQuery:_,useTableExtendedMetadataQuery:E}=v;function I(e){const t=(0,u.useRef)(!1),{data:r,isFetching:n}=y({dbId:e.dbId}),a=(0,u.useMemo)((()=>new Set(null==r?void 0:r.map((e=>{let{value:t}=e;return t})))),[r]),{dbId:s,schema:o,onSuccess:d,onError:i}=e||{},l=Boolean(s&&o&&!n&&a.has(o)),c=$({dbId:s,schema:o,forceRefresh:!1},{skip:!l}),[h]=x(),m=(0,p.Z)(((e,t)=>{null==d||d(e,t)})),b=(0,p.Z)((e=>{null==i||i(e)})),f=(0,u.useCallback)((()=>{l&&h({dbId:s,schema:o,forceRefresh:!0}).then((e=>{let{isSuccess:t,isError:r,data:n,error:a}=e;t&&n&&m(n,!0),r&&b(a)}))}),[s,o,l,m,b,h]);return(0,u.useEffect)((()=>{if(t.current){const{requestId:e,isSuccess:t,isError:r,isFetching:n,data:a,error:s,originalArgs:o}=c;null!=o&&o.forceRefresh||!e||n||(t&&a&&m(a,!1),r&&b(s))}else t.current=!0}),[c,m,b]),{...c,refetch:f}}const S=h.h.injectEndpoints({endpoints:e=>({queryValidations:e.query({providesTags:["QueryValidations"],query:e=>{let{dbId:t,schema:r,sql:n,templateParams:a}=e,s=a;try{s=JSON.parse(a||"")}catch(e){s=void 0}const o={schema:r,sql:n,...s&&{template_params:s}};return{method:"post",endpoint:`/api/v1/database/${t}/validate_sql/`,headers:{"Content-Type":"application/json"},body:JSON.stringify(o),transformResponse:e=>{let{json:t}=e;return t.result}}}})})}),{useQueryValidationsQuery:w}=S},38325:(e,t,r)=>{r.d(t,{Z:()=>a});var n=r(97654);function a(e){return(0,n.Z)(e)}}}]);
//# sourceMappingURL=faaf0ff344aed87fe6e4.chunk.js.map