


<!DOCTYPE html>
<html>
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# githubog: http://ogp.me/ns/fb/githubog#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=10">
        <title>multipolyfit/multipolyfit/core.py at master · mrocklin/multipolyfit · GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub" />
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub" />
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png" />
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png" />
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png" />
    <link rel="logo" type="image/svg" href="https://github-media-downloads.s3.amazonaws.com/github-logo.svg" />
    <meta property="og:image" content="https://github.global.ssl.fastly.net/images/modules/logos_page/Octocat.png">
    <meta name="hostname" content="github-fe115-cp1-prd.iad.github.net">
    <meta name="ruby" content="ruby 1.9.3p194-tcs-github-tcmalloc (0e75de19f8) [x86_64-linux]">
    <link rel="assets" href="https://github.global.ssl.fastly.net/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035/">
    <link rel="xhr-socket" href="/_sockets" />
    


    <meta name="msapplication-TileImage" content="/windows-tile.png" />
    <meta name="msapplication-TileColor" content="#ffffff" />
    <meta name="selected-link" value="repo_source" data-pjax-transient />
    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="BC788027:1D7C:7275107:5288EC77" name="octolytics-dimension-request_id" />
    

    
    
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />

    <meta content="authenticity_token" name="csrf-param" />
<meta content="pwkEVAqbLMv3v05pCy1wopXAGj/RuNgxxu+hmjKLaMQ=" name="csrf-token" />

    <link href="https://github.global.ssl.fastly.net/assets/github-09acd31812af6ce17b5f432a7597c5849393330e.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://github.global.ssl.fastly.net/assets/github2-5b4d8641506c5981c2f001f2dffc0306b44491c2.css" media="all" rel="stylesheet" type="text/css" />
    

    

      <script src="https://github.global.ssl.fastly.net/assets/frameworks-bca527bb59d94c16d6bf2a759779d7953fa41e76.js" type="text/javascript"></script>
      <script src="https://github.global.ssl.fastly.net/assets/github-24f11604091c33b9686ff315cd7d46a5aa9712a7.js" type="text/javascript"></script>
      
      <meta http-equiv="x-pjax-version" content="d73cf633e128aec1e0702abcc0e1de33">

        <link data-pjax-transient rel='permalink' href='/mrocklin/multipolyfit/blob/e4cd48382f2a2be296c50d6d65bedcf5b52afd50/multipolyfit/core.py'>
  <meta property="og:title" content="multipolyfit"/>
  <meta property="og:type" content="githubog:gitrepository"/>
  <meta property="og:url" content="https://github.com/mrocklin/multipolyfit"/>
  <meta property="og:image" content="https://github.global.ssl.fastly.net/images/gravatars/gravatar-user-420.png"/>
  <meta property="og:site_name" content="GitHub"/>
  <meta property="og:description" content="multipolyfit - A multivariate polynomial regression function in python"/>

  <meta name="description" content="multipolyfit - A multivariate polynomial regression function in python" />

  <meta content="306380" name="octolytics-dimension-user_id" /><meta content="mrocklin" name="octolytics-dimension-user_login" /><meta content="4631492" name="octolytics-dimension-repository_id" /><meta content="mrocklin/multipolyfit" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="4631492" name="octolytics-dimension-repository_network_root_id" /><meta content="mrocklin/multipolyfit" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/mrocklin/multipolyfit/commits/master.atom" rel="alternate" title="Recent Commits to multipolyfit:master" type="application/atom+xml" />

  </head>


  <body class="logged_out  env-production windows vis-public  page-blob">
    <div class="wrapper">
      
      
      
      


      
      <div class="header header-logged-out">
  <div class="container clearfix">

    <a class="header-logo-wordmark" href="https://github.com/">
      <span class="mega-octicon octicon-logo-github"></span>
    </a>

    <div class="header-actions">
        <a class="button primary" href="/join">Sign up</a>
      <a class="button signin" href="/login?return_to=%2Fmrocklin%2Fmultipolyfit%2Fblob%2Fmaster%2Fmultipolyfit%2Fcore.py">Sign in</a>
    </div>

    <div class="command-bar js-command-bar  in-repository">

      <ul class="top-nav">
          <li class="explore"><a href="/explore">Explore</a></li>
        <li class="features"><a href="/features">Features</a></li>
          <li class="enterprise"><a href="https://enterprise.github.com/">Enterprise</a></li>
          <li class="blog"><a href="/blog">Blog</a></li>
      </ul>
        <form accept-charset="UTF-8" action="/search" class="command-bar-form" id="top_search_form" method="get">

<input type="text" data-hotkey="/ s" name="q" id="js-command-bar-field" placeholder="Search or type a command" tabindex="1" autocapitalize="off"
    
    
      data-repo="mrocklin/multipolyfit"
      data-branch="master"
      data-sha="4d8e172e45d4a410cfbc64685111fdfe4c3ccd35"
  >

    <input type="hidden" name="nwo" value="mrocklin/multipolyfit" />

    <div class="select-menu js-menu-container js-select-menu search-context-select-menu">
      <span class="minibutton select-menu-button js-menu-target">
        <span class="js-select-button">This repository</span>
      </span>

      <div class="select-menu-modal-holder js-menu-content js-navigation-container">
        <div class="select-menu-modal">

          <div class="select-menu-item js-navigation-item js-this-repository-navigation-item selected">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" class="js-search-this-repository" name="search_target" value="repository" checked="checked" />
            <div class="select-menu-item-text js-select-button-text">This repository</div>
          </div> <!-- /.select-menu-item -->

          <div class="select-menu-item js-navigation-item js-all-repositories-navigation-item">
            <span class="select-menu-item-icon octicon octicon-check"></span>
            <input type="radio" name="search_target" value="global" />
            <div class="select-menu-item-text js-select-button-text">All repositories</div>
          </div> <!-- /.select-menu-item -->

        </div>
      </div>
    </div>

  <span class="octicon help tooltipped downwards" title="Show command bar help">
    <span class="octicon octicon-question"></span>
  </span>


  <input type="hidden" name="ref" value="cmdform">

</form>
    </div>

  </div>
</div>


      


          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        

<ul class="pagehead-actions">


  <li>
    <a href="/login?return_to=%2Fmrocklin%2Fmultipolyfit"
    class="minibutton with-count js-toggler-target star-button tooltipped upwards"
    title="You must be signed in to use this feature" rel="nofollow">
    <span class="octicon octicon-star"></span>Star
  </a>

    <a class="social-count js-social-count" href="/mrocklin/multipolyfit/stargazers">
      8
    </a>

  </li>

    <li>
      <a href="/login?return_to=%2Fmrocklin%2Fmultipolyfit"
        class="minibutton with-count js-toggler-target fork-button tooltipped upwards"
        title="You must be signed in to fork a repository" rel="nofollow">
        <span class="octicon octicon-git-branch"></span>Fork
      </a>
      <a href="/mrocklin/multipolyfit/network" class="social-count">
        3
      </a>
    </li>
</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="repo-label"><span>public</span></span>
          <span class="mega-octicon octicon-repo"></span>
          <span class="author">
            <a href="/mrocklin" class="url fn" itemprop="url" rel="author"><span itemprop="title">mrocklin</span></a>
          </span>
          <span class="repohead-name-divider">/</span>
          <strong><a href="/mrocklin/multipolyfit" class="js-current-repository js-repo-home-link">multipolyfit</a></strong>

          <span class="page-context-loader">
            <img alt="Octocat-spinner-32" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">

      <div class="repository-with-sidebar repo-container ">

        <div class="repository-sidebar">
            

<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped leftwards" title="Code">
        <a href="/mrocklin/multipolyfit" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-gotokey="c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_tags repo_branches /mrocklin/multipolyfit">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

        <li class="tooltipped leftwards" title="Issues">
          <a href="/mrocklin/multipolyfit/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="i" data-selected-links="repo_issues /mrocklin/multipolyfit/issues">
            <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>

      <li class="tooltipped leftwards" title="Pull Requests"><a href="/mrocklin/multipolyfit/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-gotokey="p" data-selected-links="repo_pulls /mrocklin/multipolyfit/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class='counter'>0</span>
            <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped leftwards" title="Pulse">
        <a href="/mrocklin/multipolyfit/pulse" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /mrocklin/multipolyfit/pulse">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" title="Graphs">
        <a href="/mrocklin/multipolyfit/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /mrocklin/multipolyfit/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped leftwards" title="Network">
        <a href="/mrocklin/multipolyfit/network" aria-label="Network" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-selected-links="repo_network /mrocklin/multipolyfit/network">
          <span class="octicon octicon-git-branch"></span> <span class="full-word">Network</span>
          <img alt="Octocat-spinner-32" class="mini-loader" height="16" src="https://github.global.ssl.fastly.net/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


  </div>
</div>

            <div class="only-with-full-nav">
              

  

<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><strong>HTTPS</strong> clone URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/mrocklin/multipolyfit.git" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/mrocklin/multipolyfit.git" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>

  

<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><strong>Subversion</strong> checkout URL</h3>
  <div class="clone-url-box">
    <input type="text" class="clone js-url-field"
           value="https://github.com/mrocklin/multipolyfit" readonly="readonly">

    <span class="js-zeroclipboard url-box-clippy minibutton zeroclipboard-button" data-clipboard-text="https://github.com/mrocklin/multipolyfit" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>,
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <span class="octicon help tooltipped upwards" title="Get help on which URL is right for you.">
    <a href="https://help.github.com/articles/which-remote-url-should-i-use">
    <span class="octicon octicon-question"></span>
    </a>
  </span>
</p>


  <a href="http://windows.github.com" class="minibutton sidebar-button">
    <span class="octicon octicon-device-desktop"></span>
    Clone in Desktop
  </a>

              <a href="/mrocklin/multipolyfit/archive/master.zip"
                 class="minibutton sidebar-button"
                 title="Download this repository as a zip file"
                 rel="nofollow">
                <span class="octicon octicon-cloud-download"></span>
                Download ZIP
              </a>
            </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          


<!-- blob contrib key: blob_contributors:v21:2dc15305ad50bc7c49cc87f22905acb3 -->

<p title="This is a placeholder element" class="js-history-link-replace hidden"></p>

<a href="/mrocklin/multipolyfit/find/master" data-pjax data-hotkey="t" class="js-show-file-finder" style="display:none">Show File Finder</a>

<div class="file-navigation">
  
  

<div class="select-menu js-menu-container js-select-menu" >
  <span class="minibutton select-menu-button js-menu-target" data-hotkey="w"
    data-master-branch="master"
    data-ref="master"
    role="button" aria-label="Switch branches or tags" tabindex="0">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button">master</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax>

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-remove-close js-menu-close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item selected">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/mrocklin/multipolyfit/blob/master/multipolyfit/core.py"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text js-select-button-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/mrocklin/multipolyfit" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">multipolyfit</span></a></span></span><span class="separator"> / </span><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/mrocklin/multipolyfit/tree/master/multipolyfit" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">multipolyfit</span></a></span><span class="separator"> / </span><strong class="final-path">core.py</strong> <span class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="multipolyfit/core.py" data-copied-hint="copied!" title="copy to clipboard"><span class="octicon octicon-clippy"></span></span>
  </div>
</div>



  <div class="commit file-history-tease">
    <img class="main-avatar" height="24" src="https://0.gravatar.com/avatar/8749ec52cee260c4c1f67f2dec29d957?d=https%3A%2F%2Fidenticons.github.com%2Fcc87617bc853aefa52cd1cc54b1c8908.png&amp;r=x&amp;s=140" width="24" />
    <span class="author"><a href="/mrocklin" rel="author">mrocklin</a></span>
    <time class="js-relative-date" datetime="2013-04-30T13:48:02-07:00" title="2013-04-30 13:48:02">April 30, 2013</time>
    <div class="commit-title">
        <a href="/mrocklin/multipolyfit/commit/8ff7dea15e9d279a3dad6d14fb73cbd1e530c134" class="message" data-pjax="true" title="standardize directory structure">standardize directory structure</a>
    </div>

    <div class="participation">
      <p class="quickstat"><a href="#blob_contributors_box" rel="facebox"><strong>1</strong> contributor</a></p>
      
    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img height="24" src="https://0.gravatar.com/avatar/8749ec52cee260c4c1f67f2dec29d957?d=https%3A%2F%2Fidenticons.github.com%2Fcc87617bc853aefa52cd1cc54b1c8908.png&amp;r=x&amp;s=140" width="24" />
            <a href="/mrocklin">mrocklin</a>
          </li>
      </ul>
    </div>
  </div>

<div id="files" class="bubble">
  <div class="file">
    <div class="meta">
      <div class="info">
        <span class="icon"><b class="octicon octicon-file-text"></b></span>
        <span class="mode" title="File Mode">file</span>
          <span>97 lines (78 sloc)</span>
        <span>3.095 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
            <a class="minibutton tooltipped leftwards"
               href="http://windows.github.com" title="Open this file in GitHub for Windows">
                <span class="octicon octicon-device-desktop"></span> Open
            </a>
              <a class="minibutton disabled tooltipped leftwards" href="#"
                 title="You must be signed in to make or propose changes">Edit</a>
          <a href="/mrocklin/multipolyfit/raw/master/multipolyfit/core.py" class="button minibutton " id="raw-url">Raw</a>
            <a href="/mrocklin/multipolyfit/blame/master/multipolyfit/core.py" class="button minibutton ">Blame</a>
          <a href="/mrocklin/multipolyfit/commits/master/multipolyfit/core.py" class="button minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->
          <a class="minibutton danger disabled empty-icon tooltipped leftwards" href="#"
             title="You must be signed in and on a branch to make or propose changes">
          Delete
        </a>
      </div><!-- /.actions -->

    </div>
        <div class="blob-wrapper data type-python js-blob-data">
        <table class="file-code file-diff">
          <tr class="file-code-line">
            <td class="blob-line-nums">
              <span id="L1" rel="#L1">1</span>
<span id="L2" rel="#L2">2</span>
<span id="L3" rel="#L3">3</span>
<span id="L4" rel="#L4">4</span>
<span id="L5" rel="#L5">5</span>
<span id="L6" rel="#L6">6</span>
<span id="L7" rel="#L7">7</span>
<span id="L8" rel="#L8">8</span>
<span id="L9" rel="#L9">9</span>
<span id="L10" rel="#L10">10</span>
<span id="L11" rel="#L11">11</span>
<span id="L12" rel="#L12">12</span>
<span id="L13" rel="#L13">13</span>
<span id="L14" rel="#L14">14</span>
<span id="L15" rel="#L15">15</span>
<span id="L16" rel="#L16">16</span>
<span id="L17" rel="#L17">17</span>
<span id="L18" rel="#L18">18</span>
<span id="L19" rel="#L19">19</span>
<span id="L20" rel="#L20">20</span>
<span id="L21" rel="#L21">21</span>
<span id="L22" rel="#L22">22</span>
<span id="L23" rel="#L23">23</span>
<span id="L24" rel="#L24">24</span>
<span id="L25" rel="#L25">25</span>
<span id="L26" rel="#L26">26</span>
<span id="L27" rel="#L27">27</span>
<span id="L28" rel="#L28">28</span>
<span id="L29" rel="#L29">29</span>
<span id="L30" rel="#L30">30</span>
<span id="L31" rel="#L31">31</span>
<span id="L32" rel="#L32">32</span>
<span id="L33" rel="#L33">33</span>
<span id="L34" rel="#L34">34</span>
<span id="L35" rel="#L35">35</span>
<span id="L36" rel="#L36">36</span>
<span id="L37" rel="#L37">37</span>
<span id="L38" rel="#L38">38</span>
<span id="L39" rel="#L39">39</span>
<span id="L40" rel="#L40">40</span>
<span id="L41" rel="#L41">41</span>
<span id="L42" rel="#L42">42</span>
<span id="L43" rel="#L43">43</span>
<span id="L44" rel="#L44">44</span>
<span id="L45" rel="#L45">45</span>
<span id="L46" rel="#L46">46</span>
<span id="L47" rel="#L47">47</span>
<span id="L48" rel="#L48">48</span>
<span id="L49" rel="#L49">49</span>
<span id="L50" rel="#L50">50</span>
<span id="L51" rel="#L51">51</span>
<span id="L52" rel="#L52">52</span>
<span id="L53" rel="#L53">53</span>
<span id="L54" rel="#L54">54</span>
<span id="L55" rel="#L55">55</span>
<span id="L56" rel="#L56">56</span>
<span id="L57" rel="#L57">57</span>
<span id="L58" rel="#L58">58</span>
<span id="L59" rel="#L59">59</span>
<span id="L60" rel="#L60">60</span>
<span id="L61" rel="#L61">61</span>
<span id="L62" rel="#L62">62</span>
<span id="L63" rel="#L63">63</span>
<span id="L64" rel="#L64">64</span>
<span id="L65" rel="#L65">65</span>
<span id="L66" rel="#L66">66</span>
<span id="L67" rel="#L67">67</span>
<span id="L68" rel="#L68">68</span>
<span id="L69" rel="#L69">69</span>
<span id="L70" rel="#L70">70</span>
<span id="L71" rel="#L71">71</span>
<span id="L72" rel="#L72">72</span>
<span id="L73" rel="#L73">73</span>
<span id="L74" rel="#L74">74</span>
<span id="L75" rel="#L75">75</span>
<span id="L76" rel="#L76">76</span>
<span id="L77" rel="#L77">77</span>
<span id="L78" rel="#L78">78</span>
<span id="L79" rel="#L79">79</span>
<span id="L80" rel="#L80">80</span>
<span id="L81" rel="#L81">81</span>
<span id="L82" rel="#L82">82</span>
<span id="L83" rel="#L83">83</span>
<span id="L84" rel="#L84">84</span>
<span id="L85" rel="#L85">85</span>
<span id="L86" rel="#L86">86</span>
<span id="L87" rel="#L87">87</span>
<span id="L88" rel="#L88">88</span>
<span id="L89" rel="#L89">89</span>
<span id="L90" rel="#L90">90</span>
<span id="L91" rel="#L91">91</span>
<span id="L92" rel="#L92">92</span>
<span id="L93" rel="#L93">93</span>
<span id="L94" rel="#L94">94</span>
<span id="L95" rel="#L95">95</span>
<span id="L96" rel="#L96">96</span>

            </td>
            <td class="blob-line-code">
                    <div class="highlight"><pre><div class='line' id='LC1'><span class="kn">from</span> <span class="nn">numpy</span> <span class="kn">import</span> <span class="n">linalg</span><span class="p">,</span> <span class="n">zeros</span><span class="p">,</span> <span class="n">ones</span><span class="p">,</span> <span class="n">hstack</span><span class="p">,</span> <span class="n">asarray</span></div><div class='line' id='LC2'><span class="kn">import</span> <span class="nn">itertools</span></div><div class='line' id='LC3'><br/></div><div class='line' id='LC4'><span class="k">def</span> <span class="nf">basis_vector</span><span class="p">(</span><span class="n">n</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></div><div class='line' id='LC5'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot; Return an array like [0, 0, ..., 1, ..., 0, 0]</span></div><div class='line' id='LC6'><br/></div><div class='line' id='LC7'><span class="sd">    &gt;&gt;&gt; from multipolyfit.core import basis_vector</span></div><div class='line' id='LC8'><span class="sd">    &gt;&gt;&gt; basis_vector(3, 1)</span></div><div class='line' id='LC9'><span class="sd">    array([0, 1, 0])</span></div><div class='line' id='LC10'><span class="sd">    &gt;&gt;&gt; basis_vector(5, 4)</span></div><div class='line' id='LC11'><span class="sd">    array([0, 0, 0, 0, 1])</span></div><div class='line' id='LC12'><span class="sd">    &quot;&quot;&quot;</span></div><div class='line' id='LC13'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">x</span> <span class="o">=</span> <span class="n">zeros</span><span class="p">(</span><span class="n">n</span><span class="p">,</span> <span class="n">dtype</span><span class="o">=</span><span class="nb">int</span><span class="p">)</span></div><div class='line' id='LC14'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">x</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">=</span> <span class="mi">1</span></div><div class='line' id='LC15'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">x</span></div><div class='line' id='LC16'><br/></div><div class='line' id='LC17'><span class="k">def</span> <span class="nf">as_tall</span><span class="p">(</span><span class="n">x</span><span class="p">):</span></div><div class='line' id='LC18'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot; Turns a row vector into a column vector &quot;&quot;&quot;</span></div><div class='line' id='LC19'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">x</span><span class="o">.</span><span class="n">reshape</span><span class="p">(</span><span class="n">x</span><span class="o">.</span><span class="n">shape</span> <span class="o">+</span> <span class="p">(</span><span class="mi">1</span><span class="p">,))</span></div><div class='line' id='LC20'><br/></div><div class='line' id='LC21'><span class="k">def</span> <span class="nf">multipolyfit</span><span class="p">(</span><span class="n">xs</span><span class="p">,</span> <span class="n">y</span><span class="p">,</span> <span class="n">deg</span><span class="p">,</span> <span class="n">full</span><span class="o">=</span><span class="bp">False</span><span class="p">,</span> <span class="n">model_out</span><span class="o">=</span><span class="bp">False</span><span class="p">,</span> <span class="n">powers_out</span><span class="o">=</span><span class="bp">False</span><span class="p">):</span></div><div class='line' id='LC22'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot;</span></div><div class='line' id='LC23'><span class="sd">    Least squares multivariate polynomial fit</span></div><div class='line' id='LC24'><br/></div><div class='line' id='LC25'><span class="sd">    Fit a polynomial like ``y = a**2 + 3a - 2ab + 4b**2 - 1``</span></div><div class='line' id='LC26'><span class="sd">    with many covariates a, b, c, ...</span></div><div class='line' id='LC27'><br/></div><div class='line' id='LC28'><span class="sd">    Parameters</span></div><div class='line' id='LC29'><span class="sd">    ----------</span></div><div class='line' id='LC30'><br/></div><div class='line' id='LC31'><span class="sd">    xs : array_like, shape (M, k)</span></div><div class='line' id='LC32'><span class="sd">         x-coordinates of the k covariates over the M sample points</span></div><div class='line' id='LC33'><span class="sd">    y :  array_like, shape(M,)</span></div><div class='line' id='LC34'><span class="sd">         y-coordinates of the sample points.</span></div><div class='line' id='LC35'><span class="sd">    deg : int</span></div><div class='line' id='LC36'><span class="sd">         Degree o fthe fitting polynomial</span></div><div class='line' id='LC37'><span class="sd">    model_out : bool (defaults to True)</span></div><div class='line' id='LC38'><span class="sd">         If True return a callable function</span></div><div class='line' id='LC39'><span class="sd">         If False return an array of coefficients</span></div><div class='line' id='LC40'><span class="sd">    powers_out : bool (defaults to False)</span></div><div class='line' id='LC41'><span class="sd">         Returns the meaning of each of the coefficients in the form of an</span></div><div class='line' id='LC42'><span class="sd">         iterator that gives the powers over the inputs and 1</span></div><div class='line' id='LC43'><span class="sd">         For example if xs corresponds to the covariates a,b,c then the array</span></div><div class='line' id='LC44'><span class="sd">         [1, 2, 1, 0] corresponds to 1**1 * a**2 * b**1 * c**0</span></div><div class='line' id='LC45'><br/></div><div class='line' id='LC46'><span class="sd">    See Also</span></div><div class='line' id='LC47'><span class="sd">    --------</span></div><div class='line' id='LC48'><span class="sd">        numpy.polyfit</span></div><div class='line' id='LC49'><br/></div><div class='line' id='LC50'><span class="sd">    &quot;&quot;&quot;</span></div><div class='line' id='LC51'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">y</span> <span class="o">=</span> <span class="n">asarray</span><span class="p">(</span><span class="n">y</span><span class="p">)</span><span class="o">.</span><span class="n">squeeze</span><span class="p">()</span></div><div class='line' id='LC52'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">rows</span> <span class="o">=</span> <span class="n">y</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span></div><div class='line' id='LC53'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs</span> <span class="o">=</span> <span class="n">asarray</span><span class="p">(</span><span class="n">xs</span><span class="p">)</span></div><div class='line' id='LC54'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">num_covariates</span> <span class="o">=</span> <span class="n">xs</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span></div><div class='line' id='LC55'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs</span> <span class="o">=</span> <span class="n">hstack</span><span class="p">((</span><span class="n">ones</span><span class="p">((</span><span class="n">xs</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="mi">1</span><span class="p">),</span> <span class="n">dtype</span><span class="o">=</span><span class="n">xs</span><span class="o">.</span><span class="n">dtype</span><span class="p">)</span> <span class="p">,</span> <span class="n">xs</span><span class="p">))</span></div><div class='line' id='LC56'><br/></div><div class='line' id='LC57'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">generators</span> <span class="o">=</span> <span class="p">[</span><span class="n">basis_vector</span><span class="p">(</span><span class="n">num_covariates</span><span class="o">+</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span></div><div class='line' id='LC58'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">num_covariates</span><span class="o">+</span><span class="mi">1</span><span class="p">)]</span></div><div class='line' id='LC59'><br/></div><div class='line' id='LC60'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># All combinations of degrees</span></div><div class='line' id='LC61'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">powers</span> <span class="o">=</span> <span class="nb">map</span><span class="p">(</span><span class="nb">sum</span><span class="p">,</span> <span class="n">itertools</span><span class="o">.</span><span class="n">combinations_with_replacement</span><span class="p">(</span><span class="n">generators</span><span class="p">,</span> <span class="n">deg</span><span class="p">))</span></div><div class='line' id='LC62'><br/></div><div class='line' id='LC63'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># Raise data to specified degree pattern, stack in order</span></div><div class='line' id='LC64'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">A</span> <span class="o">=</span> <span class="n">hstack</span><span class="p">(</span><span class="n">asarray</span><span class="p">([</span><span class="n">as_tall</span><span class="p">((</span><span class="n">xs</span><span class="o">**</span><span class="n">p</span><span class="p">)</span><span class="o">.</span><span class="n">prod</span><span class="p">(</span><span class="mi">1</span><span class="p">))</span> <span class="k">for</span> <span class="n">p</span> <span class="ow">in</span> <span class="n">powers</span><span class="p">]))</span></div><div class='line' id='LC65'><br/></div><div class='line' id='LC66'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">beta</span> <span class="o">=</span> <span class="n">linalg</span><span class="o">.</span><span class="n">lstsq</span><span class="p">(</span><span class="n">A</span><span class="p">,</span> <span class="n">y</span><span class="p">)[</span><span class="mi">0</span><span class="p">]</span></div><div class='line' id='LC67'><br/></div><div class='line' id='LC68'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">model_out</span><span class="p">:</span></div><div class='line' id='LC69'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">mk_model</span><span class="p">(</span><span class="n">beta</span><span class="p">,</span> <span class="n">powers</span><span class="p">)</span></div><div class='line' id='LC70'><br/></div><div class='line' id='LC71'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="n">powers_out</span><span class="p">:</span></div><div class='line' id='LC72'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">beta</span><span class="p">,</span> <span class="n">powers</span></div><div class='line' id='LC73'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">beta</span></div><div class='line' id='LC74'><br/></div><div class='line' id='LC75'><span class="k">def</span> <span class="nf">mk_model</span><span class="p">(</span><span class="n">beta</span><span class="p">,</span> <span class="n">powers</span><span class="p">):</span></div><div class='line' id='LC76'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="sd">&quot;&quot;&quot; Create a callable python function out of beta/powers from multipolyfit</span></div><div class='line' id='LC77'><br/></div><div class='line' id='LC78'><span class="sd">    This function is callable from within multipolyfit using the model_out flag</span></div><div class='line' id='LC79'><span class="sd">    &quot;&quot;&quot;</span></div><div class='line' id='LC80'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># Create a function that takes in many x values</span></div><div class='line' id='LC81'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="c"># and returns an approximate y value</span></div><div class='line' id='LC82'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">def</span> <span class="nf">model</span><span class="p">(</span><span class="o">*</span><span class="n">args</span><span class="p">):</span></div><div class='line' id='LC83'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">num_covariates</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">powers</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span> <span class="o">-</span> <span class="mi">1</span></div><div class='line' id='LC84'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">args</span><span class="p">)</span><span class="o">!=</span><span class="p">(</span><span class="n">num_covariates</span><span class="p">):</span></div><div class='line' id='LC85'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s">&quot;Expected </span><span class="si">%d</span><span class="s"> inputs&quot;</span><span class="o">%</span><span class="n">num_covariates</span><span class="p">)</span></div><div class='line' id='LC86'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs</span> <span class="o">=</span> <span class="n">asarray</span><span class="p">((</span><span class="mi">1</span><span class="p">,)</span> <span class="o">+</span> <span class="n">args</span><span class="p">)</span></div><div class='line' id='LC87'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="nb">sum</span><span class="p">([</span><span class="n">coeff</span> <span class="o">*</span> <span class="p">(</span><span class="n">xs</span><span class="o">**</span><span class="n">p</span><span class="p">)</span><span class="o">.</span><span class="n">prod</span><span class="p">()</span></div><div class='line' id='LC88'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="n">p</span><span class="p">,</span> <span class="n">coeff</span> <span class="ow">in</span> <span class="nb">zip</span><span class="p">(</span><span class="n">powers</span><span class="p">,</span> <span class="n">beta</span><span class="p">)])</span></div><div class='line' id='LC89'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">model</span></div><div class='line' id='LC90'><br/></div><div class='line' id='LC91'><span class="k">def</span> <span class="nf">mk_sympy_function</span><span class="p">(</span><span class="n">beta</span><span class="p">,</span> <span class="n">powers</span><span class="p">):</span></div><div class='line' id='LC92'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="kn">from</span> <span class="nn">sympy</span> <span class="kn">import</span> <span class="n">symbols</span><span class="p">,</span> <span class="n">Add</span><span class="p">,</span> <span class="n">Mul</span><span class="p">,</span> <span class="n">S</span></div><div class='line' id='LC93'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">num_covariates</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">powers</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span> <span class="o">-</span> <span class="mi">1</span></div><div class='line' id='LC94'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="n">xs</span> <span class="o">=</span> <span class="p">(</span><span class="n">S</span><span class="o">.</span><span class="n">One</span><span class="p">,)</span> <span class="o">+</span> <span class="n">symbols</span><span class="p">(</span><span class="s">&#39;x0:</span><span class="si">%d</span><span class="s">&#39;</span><span class="o">%</span><span class="n">num_covariates</span><span class="p">)</span></div><div class='line' id='LC95'>&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">return</span> <span class="n">Add</span><span class="p">(</span><span class="o">*</span><span class="p">[</span><span class="n">coeff</span> <span class="o">*</span> <span class="n">Mul</span><span class="p">(</span><span class="o">*</span><span class="p">[</span><span class="n">x</span><span class="o">**</span><span class="n">deg</span> <span class="k">for</span> <span class="n">x</span><span class="p">,</span> <span class="n">deg</span> <span class="ow">in</span> <span class="nb">zip</span><span class="p">(</span><span class="n">xs</span><span class="p">,</span> <span class="n">power</span><span class="p">)])</span></div><div class='line' id='LC96'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="k">for</span> <span class="n">power</span><span class="p">,</span> <span class="n">coeff</span> <span class="ow">in</span> <span class="nb">zip</span><span class="p">(</span><span class="n">powers</span><span class="p">,</span> <span class="n">beta</span><span class="p">)])</span></div></pre></div>
            </td>
          </tr>
        </table>
  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" class="js-jump-to-line" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/">
      <span class="mega-octicon octicon-mark-github"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2013 <span title="0.02872s from github-fe115-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-fullscreen-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="js-fullscreen-contents" placeholder="" data-suggester="fullscreen_suggester"></textarea>
          <div class="suggester-container">
              <div class="suggester fullscreen-suggester js-navigation-container" id="fullscreen_suggester"
                 data-url="/mrocklin/multipolyfit/suggestions/commit">
              </div>
          </div>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped leftwards" title="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped leftwards"
      title="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-remove-close close ajax-error-dismiss"></a>
      Something went wrong with that request. Please try again.
    </div>

  </body>
</html>

