import{L as ee,P as te,r as i,N as se,I as B,z as v,c as d,B as e,A as t,E as p,o as u,K as I,F as Z,C as z,G as _,R as le,V as f,T as oe,$ as ae,u as j,a0 as F}from"./index-DX0kaMnH.js";const ne={class:"grid"},ie={class:"col-12"},re={class:"card"},de=e("div",{class:"my-2"},[e("h4",{class:"text-2xl font-raleway font-bold text-devanga-primary"}," Manage Events ")],-1),ue={class:"flex justify-end"},ce={class:"flex flex-col"},ve={class:"md:w-40 relative"},pe=["src","alt"],me={class:"flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6"},_e={class:"flex flex-row md:flex-col justify-between items-start gap-2"},fe={class:"font-medium text-surface-500 dark:text-surface-400 text-sm"},xe={class:"text-lg font-medium mt-2"},ge={class:"bg-surface-100 p-1",style:{"border-radius":"30px"}},he={class:"bg-surface-0 flex items-center gap-2 justify-center py-1 px-2",style:{"border-radius":"30px","box-shadow":`0px 1px 2px 0px rgba(0, 0, 0, 0.04),
                                0px 1px 2px 0px rgba(0, 0, 0, 0.06)`}},ye={class:"text-surface-900 font-medium text-sm"},be=e("i",{class:"pi pi-star-fill text-yellow-500"},null,-1),we={class:"flex flex-col md:items-end gap-8"},ke={class:"text-xl font-semibold"},Ee={class:"flex flex-row-reverse md:flex-row gap-2"},Ve={class:"grid grid-cols-12 gap-4"},Ce={class:"p-6 border border-surface-200 dark:border-surface-700 bg-surface-0 dark:bg-surface-900 rounded flex flex-col"},De={class:"bg-surface-50 flex justify-center rounded p-4"},Te={class:"relative mx-auto"},Se=["src","alt"],Ue={class:"pt-6"},Ie={class:"flex flex-row justify-between items-start gap-2"},Ne={class:"font-medium text-surface-500 dark:text-surface-400 text-sm"},qe={class:"text-lg font-medium mt-1"},Be={class:"bg-surface-100 p-1",style:{"border-radius":"30px"}},je={class:"bg-surface-0 flex items-center gap-2 justify-center py-1 px-2",style:{"border-radius":"30px","box-shadow":`0px 1px 2px 0px rgba(0, 0, 0, 0.04),
                                0px 1px 2px 0px rgba(0, 0, 0, 0.06)`}},Fe={class:"text-surface-900 font-medium text-sm"},Me=e("i",{class:"pi pi-star-fill text-yellow-500"},null,-1),Oe={class:"flex flex-col gap-6 mt-6"},Pe={class:"text-2xl font-semibold"},Re={class:"flex gap-2"},$e={class:"field py-2"},Le=e("label",{for:"eventname"},"Event Name",-1),Ze={key:0,class:"p-invalid"},ze={class:"field py-2"},Ae=e("label",{for:"eventprice"},"Event Price in TZS",-1),Ge={key:0,class:"p-invalid"},Ke={class:"field py-2"},He=e("label",{for:"eventdescription"},"Event Description",-1),Je={class:"field py-2"},Qe=e("label",{for:"eventname"},"Event Type",-1),We=e("option",{selected:""},"Choose event type",-1),Xe=e("option",{value:"online"},"Online Event",-1),Ye=e("option",{value:"on_premises"},"On Premises Event",-1),et=[We,Xe,Ye],tt={key:0,class:"field py-2"},st=e("label",{for:"eventname"},"Event Location",-1),lt={key:0,class:"p-invalid"},ot={class:"flex space-x-4 justify-between"},at={class:"field py-2"},nt=e("label",{for:"eventstartdate"},"Event Start Date",-1),it={key:0,class:"p-invalid"},rt={class:"field py-2"},dt=e("label",{for:"eventendtdate"},"Event End Date",-1),ut={key:0,class:"p-invalid"},ct={class:"field py-2"},vt=e("label",{for:"registrationDeadline"},"Registration Deadline",-1),pt={key:0,class:"p-invalid"},mt={class:"field py-2"},_t=e("label",{for:"eventcover"},"Course Image",-1),ft={key:0,class:"p-invalid"},xt={class:"mt-3"},gt=e("div",{class:"confirmation-content"},[e("p",null,"Are you sure you want to delete this course?")],-1),ht={class:"p-dialog-footer"},wt={__name:"ManageEvent",setup(yt){const g=ee();te();const M=i([]),h=i(!1),D=i(!1),O=i({}),y=i(null),b=i(""),w=i(""),c=i(""),x=i(null),k=i(null),E=i(null),V=i(null),r=i(!1),N=i("grid"),A=i(["list","grid"]);se(()=>{q()});const q=()=>{B.get("coaching/events/").then(o=>{M.value=o.data}).catch(o=>{console.error("Error fetching events:",o)})},G=()=>{if(r.value=!0,!c.value||!x.value||!b.value||!y.value)return;const o=new FormData;o.append("title",c.value),o.append("price",x.value.toFixed(2)),o.append("description",b.value),o.append("event_type",w.value);const l=m=>{if(!m)return null;const C=new Date(m);return isNaN(C.getTime())?null:C.toISOString()},n=l(k.value),T=l(E.value),S=l(V.value);if(!n||!T||!S){g.add({severity:"error",summary:"Error",detail:"Invalid date value",life:3e3});return}o.append("start_time",n),o.append("end_time",T),o.append("registration_deadline",S),o.append("location",w.value),o.append("cover",y.value),B.post("coaching/events/",o,{headers:{"Content-Type":"multipart/form-data"}}).then(m=>{g.add({severity:"success",summary:"Successful",detail:"Course saved successfully",life:3e3}),q(),h.value=!1,P()}).catch(m=>{console.error("Error saving course:",m),g.add({severity:"error",summary:"Error",detail:"Error saving course",life:3e3})})},K=o=>{o.target.files.length>0&&(y.value=o.target.files[0])},P=()=>{c.value="",x.value=null,b.value="",y.value=null,k.value=null,E.value=null,V.value=null,r.value=!1},H=()=>{O.value={},r.value=!1,h.value=!0},R=()=>{h.value=!1,D.value=!1,r.value=!1,P()},J=()=>{B.delete(`course/${O.value.id}`).then(o=>{g.add({severity:"success",summary:"Successful",detail:"Course Deleted",life:3e3}),q(),D.value=!1}).catch(o=>{console.error("Error deleting course:",o),g.add({severity:"error",summary:"Error",detail:"Error deleting course",life:3e3})})},Q=()=>{};return(o,l)=>{const n=v("Button"),T=v("Toolbar"),S=v("SelectButton"),m=v("Tag"),C=v("router-link"),W=v("DataView"),$=v("InputText"),X=v("InputNumber"),Y=v("Editor"),L=v("Dialog");return u(),d("div",ne,[e("div",ie,[e("div",re,[t(T,{class:"mb-4"},{start:p(()=>[de]),end:p(()=>[t(n,{label:"New",icon:"pi pi-plus",class:"mr-2",severity:"success",onClick:H}),t(n,{label:"Export",icon:"pi pi-upload",severity:"help",onClick:Q})]),_:1}),t(W,{value:M.value,layout:N.value},{header:p(()=>[e("div",ue,[t(S,{modelValue:N.value,"onUpdate:modelValue":l[0]||(l[0]=s=>N.value=s),options:A.value,allowEmpty:!1},{option:p(({option:s})=>[e("i",{class:I([s==="list"?"pi pi-bars":"pi pi-table"])},null,2)]),_:1},8,["modelValue","options"])])]),list:p(s=>[e("div",ce,[(u(!0),d(Z,null,z(s.items,(a,U)=>(u(),d("div",{key:U},[e("div",{class:I(["flex flex-col sm:flex-row sm:items-center p-6 gap-4",{"border-t border-surface-200 dark:border-surface-700":U!==0}])},[e("div",ve,[e("img",{class:"block xl:block mx-auto rounded w-full",src:a.cover,alt:a.title},null,8,pe),t(m,{value:a.inventoryStatus,class:"absolute dark:!bg-surface-900",style:{left:"4px",top:"4px"}},null,8,["value"])]),e("div",me,[e("div",_e,[e("div",null,[e("span",fe,_(a.category),1),e("div",xe,_(a.title),1)]),e("div",ge,[e("div",he,[e("span",ye,_(a.rating),1),be])])]),e("div",we,[e("span",ke,"$"+_(a.price),1),e("div",Ee,[t(C,{to:{name:"event-detail",params:{slug:a.slug}}},{default:p(()=>[t(n,{icon:"pi pi-eye",severity:"info"})]),_:2},1032,["to"]),t(n,{icon:"pi pi-pencil"}),t(n,{icon:"pi pi-trash",severity:"danger"})])])])],2)]))),128))])]),grid:p(s=>[e("div",Ve,[(u(!0),d(Z,null,z(s.items,(a,U)=>(u(),d("div",{key:U,class:"col-span-12 sm:col-span-6 md:col-span-4 xl:col-span-4 p-2"},[e("div",Ce,[e("div",De,[e("div",Te,[e("img",{class:"rounded w-full",src:a.cover,alt:a.title,style:{"max-width":"300px"}},null,8,Se),t(m,{value:a.event_type,class:"absolute dark:!bg-surface-900",style:{left:"4px",top:"4px"}},null,8,["value"])])]),e("div",Ue,[e("div",Ie,[e("div",null,[e("span",Ne,_(a.title),1),e("div",qe,_(a.title),1)]),e("div",Be,[e("div",je,[e("span",Fe,_(a.rating),1),Me])])]),e("div",Oe,[e("span",Pe,"$"+_(a.price),1),e("div",Re,[t(C,{to:{name:"event-detail",params:{slug:a.slug}}},{default:p(()=>[t(n,{icon:"pi pi-eye",severity:"info"})]),_:2},1032,["to"]),t(n,{icon:"pi pi-pencil"}),t(n,{icon:"pi pi-trash",severity:"danger"})])])])])]))),128))])]),_:1},8,["value","layout"]),t(L,{visible:h.value,"onUpdate:visible":l[9]||(l[9]=s=>h.value=s),style:{width:"650px"},header:"Create Course",modal:!0,class:"p-fluid"},{default:p(()=>[e("form",{onSubmit:le(G,["prevent"])},[e("div",$e,[Le,t($,{id:"eventname",modelValue:c.value,"onUpdate:modelValue":l[1]||(l[1]=s=>c.value=s),modelModifiers:{trim:!0},required:"",autofocus:"",class:I({"p-invalid":r.value&&!c.value}),placeholder:"Enter Course name",name:"eventname"},null,8,["modelValue","class"]),r.value&&!c.value?(u(),d("small",Ze,"Course name is required.")):f("",!0)]),e("div",ze,[Ae,t(X,{modelValue:x.value,"onUpdate:modelValue":l[2]||(l[2]=s=>x.value=s),inputId:"currency-us",mode:"currency",currency:"TZS",locale:"en-TZ",placeholder:"120,000"},null,8,["modelValue"]),r.value&&!x.value?(u(),d("small",Ge,"Event price is required.")):f("",!0)]),e("div",Ke,[He,t(Y,{modelValue:b.value,"onUpdate:modelValue":l[3]||(l[3]=s=>b.value=s),editorStyle:"height: 200px"},null,8,["modelValue"])]),e("div",Je,[Qe,oe(e("select",{id:"countries","onUpdate:modelValue":l[4]||(l[4]=s=>w.value=s),class:"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"},et,512),[[ae,w.value]])]),w.value=="on_premises"?(u(),d("div",tt,[st,t($,{id:"eventname",modelValue:c.value,"onUpdate:modelValue":l[5]||(l[5]=s=>c.value=s),modelModifiers:{trim:!0},required:"",autofocus:"",class:I({"p-invalid":r.value&&!c.value}),placeholder:"Enter Course name",name:"eventname"},null,8,["modelValue","class"]),r.value&&!c.value?(u(),d("small",lt,"Course name is required.")):f("",!0)])):f("",!0),e("div",ot,[e("div",at,[nt,t(j(F),{id:"eventstartdate",modelValue:k.value,"onUpdate:modelValue":l[6]||(l[6]=s=>k.value=s),showTime:"",hourFormat:"24"},null,8,["modelValue"]),r.value&&!k.value?(u(),d("small",it,"Event start date is required.")):f("",!0)]),e("div",rt,[dt,t(j(F),{id:"eventendtdate",modelValue:E.value,"onUpdate:modelValue":l[7]||(l[7]=s=>E.value=s),showTime:"",hourFormat:"24"},null,8,["modelValue"]),r.value&&!E.value?(u(),d("small",ut,"Event End date is required.")):f("",!0)])]),e("div",ct,[vt,t(j(F),{id:"registrationDeadline",modelValue:V.value,"onUpdate:modelValue":l[8]||(l[8]=s=>V.value=s),showTime:"",hourFormat:"24"},null,8,["modelValue"]),r.value&&!V.value?(u(),d("small",pt,"Registration date is required.")):f("",!0)]),e("div",mt,[_t,e("input",{type:"file",name:"cover",accept:"image/*",onChange:K,ref:"files"},null,544),r.value&&!y.value?(u(),d("small",ft,"Event cover image is required.")):f("",!0)]),e("div",xt,[t(n,{label:"Save the course",icon:"pi pi-check",type:"submit",class:"m-2"}),t(n,{label:"Cancel",icon:"pi pi-times",text:"",onClick:R,class:"m-2",severity:"contrast",outlined:""})])],32)]),_:1},8,["visible"]),t(L,{visible:D.value,"onUpdate:visible":l[10]||(l[10]=s=>D.value=s),style:{width:"450px"},header:"Confirm",modal:!0},{default:p(()=>[gt,e("div",ht,[t(n,{label:"Cancel",icon:"pi pi-times",class:"p-button-text",onClick:R}),t(n,{label:"Delete",icon:"pi pi-trash",class:"p-button-danger",onClick:J})])]),_:1},8,["visible"])])])])}}};export{wt as default};