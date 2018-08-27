#!groovy?

def build_extensions() 
{
	extensionsRoot = pwd()

	// Build
	stage ('Build Extensions') 
	{
		withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
		{
			bat "mvn -f Maven/com.airbus.citrus.parent/pom.xml clean install -Dcitrus.core.root=${coreRoot} -Dcitrus.extensions.root=${extensionsRoot} -PArtal,External -U -DskipTests"		
		}
		stash includes: 'Tests/**', name: "tests"
		stash includes: 'p2/com.airbus.citrus.p2.extensions.dependencies/site/**', name: "extensions_p2"
		stash includes: 'Maven/com.airbus.citrus.parent/**', name: "extensions_maven"
	}
}

def build_products()
{
	def sigma_branch = env.BRANCH_NAME.toLowerCase().contains("sigma") || env.BRANCH_NAME.toLowerCase().contains("sgm-")
	def workman_branch = env.BRANCH_NAME.toLowerCase().contains("workman") || env.BRANCH_NAME.toLowerCase().contains("wm-")
	def xicdstudio_branch = env.BRANCH_NAME.toLowerCase().contains("xicdstudio") || env.BRANCH_NAME.toLowerCase().contains("cap-")
	def inside_branch = env.BRANCH_NAME.toLowerCase().contains("inside") || env.BRANCH_NAME.toLowerCase().contains("ins-")
	def master_branch = env.BRANCH_NAME.equals("master")
	echo "sigma_branch : ${sigma_branch}"

	// Products
	if (inside_branch || master_branch)
	{
		archive_dropins()
		build_inside()
	}
	if (!inside_branch) 
	{
		build_sigma()
	}
	
	// Validation
	try
	{
		if (sigma_branch || master_branch)
		{
			validate("Connections Validation", this.&validate_connections_windows, this.&validate_connections_linux, startedByTimer)
		} 
/*		if (xicdstudio_branch || sigma_branch || master_branch) 
		{
			validate("xICDStudio Validation", this.&validate_xicdstudio_windows, this.&validate_xicdstudio_linux, startedByTimer)
		}
		if (workman_branch || sigma_branch || master_branch) 
		{
			validate("Workman CLI Validation", this.&validate_workman_cli_windows, this.&validate_workman_cli_linux, startedByTimer)
			validate("Workman GUI Validation", this.&validate_workman_gui_windows, this.&validate_workman_gui_linux, startedByTimer)
		}*/
	}
	finally
	{
		if (master_branch || sigma_branch || xicdstudio_branch || workman_branch)
		{
			stage('SIGMA Documentation')
			{
				withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
				{
					bat "mvn -f Documentation/com.airbus.sigma.documentation.gen/pom.xml clean pre-site -Dcitrus.core.root=${coreRoot} -Dcitrus.extensions.root=${extensionsRoot} -PArtal,External"
				}
				archiveArtifacts allowEmptyArchive: true, artifacts: 'Documentation/com.airbus.sigma.documentation.gen/target/docs/**', defaultExcludes: false
			}
		}
	}

}

def archive_results()
{
	echo "Archive Reqtify reports"
	archiveArtifacts allowEmptyArchive: true, artifacts: 'Tests/**/surefire-reports/TR_*.xml', defaultExcludes: false
	echo "Archive failed tests screenshots"
	archiveArtifacts allowEmptyArchive: true, artifacts: 'Tests/**/screenshots/*.jpeg', defaultExcludes: false
}

def archive_dropins()
{
	stage('Dropins')
	{
		echo "Package sites"
		zip archive: true, dir: 'Site\\com.artal.citrus.capella.site\\target\\repository', glob: '*\\*.jar', zipFile: 'Site\\com.artal.citrus.capella.dropins.zip'
		zip archive: true, dir: 'Site\\com.artal.citrus.eagle.site\\target\\repository', glob: '*\\*.jar', zipFile: 'Site\\com.artal.citrus.eagle.dropins.zip'
		zip archive: true, dir: 'Site\\com.artal.citrus.template.testmean.site\\target\\repository', glob: '*\\*.jar', zipFile: 'Site\\com.artal.citrus.template.testmean.dropins.zip'
		//zip archive: true, dir: 'Site\\com.artal.citrus.tool.ap2633specification.site\\target\\repository', glob: '*\\*.jar', zipFile: 'Site\\com.artal.citrus.tool.ap2633specification.dropins.zip'
		zip archive: true, dir: 'Site\\com.artal.citrus.vp.simulationspecification.site\\target\\repository', glob: '*\\*.jar', zipFile: 'Site\\com.artal.citrus.vp.simulationspecification.dropins.zip'
		zip archive: true, dir: 'Site\\com.scilab.citrus.xcos.site\\target\\repository', glob: '*\\*.jar', zipFile: 'Site\\com.scilab.citrus.xcos.dropins.zip'
		
		echo "Archive Sites"
		archive 'Site\\*.zip'
	}
}

def build_inside()
{
  stage('INSIDE')
  {
		withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)])
		{
			bat "mvn -f Repository/com.airbus.citrus.inside.repository/pom.xml clean package -Dcitrus.core.root=${coreRoot} -Dcitrus.extensions.root=${extensionsRoot} -PArtal,External -U -DskipTests"
		}
		echo "Archive INSIDE product"
		archive 'Repository\\com.airbus.citrus.inside.repository\\target\\products\\*.zip'
  }
}

def build_sigma() 
{
	stage('SIGMA') 
	{
		withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
		{
			bat "mvn -f Documentation/com.airbus.sigma.intranet/pom.xml clean site -Dcitrus.core.root=${coreRoot} -Dcitrus.extensions.root=${extensionsRoot} -PArtal,External"
			bat "mvn -f Repository/com.airbus.citrus.sigma.repository/pom.xml clean integration-test -Dcitrus.core.root=${coreRoot} -Dcitrus.extensions.root=${extensionsRoot} -PArtal,External -U -DskipTests"
		}
		echo "Archive SIGMA product"
		archive 'Repository\\com.airbus.citrus.sigma.repository\\target\\products\\*.zip'
		stash includes:'Repository/com.airbus.citrus.sigma.repository/target/products/*.zip', name:'sigma_product'
	}
}

def validate(String stage_name, Closure validate_windows, Closure validate_linux, boolean nightly)
{
	try
	{
		stage(stage_name)
		{
			parallel win32_x86_64:
			{
				validate_windows(nightly)
			}/*, linux_x86_64:
			{
				node_labels = 'citrus && RHEL7'
				if (nightly)
				{
					node_labels += ' && citrus_ref'
				}
				node(node_labels) 
				{
					deleteDir()
					unstash 'repository'
					dir ('citrus.core')
					{
						coreRoot = pwd()
						unstash 'deltapack_p2'
						unstash 'core_repository'
					}
					dir ('citrus.extensions')
					{
						extensionsRoot = pwd()
						unstash 'extensions_p2'
						unstash 'extensions_maven'
						unstash 'tests'
						unstash 'sigma_product'
						validate_linux(nightly)
					}
				}
			}*/
		}
	}
	catch (err)
	{
		echo "Caught: ${err}"
		if (!currentBuild.result.equals('ABORTED'))
		{	  
			currentBuild.result = 'FAILURE'
		}
		else
		{
			throw err
		}
	}
	finally
	{
		archive_results()
	}
}

def validate_xicdstudio_windows(boolean nightly)
{
	def nightlyProfiles = ""
	if (nightly)
	{
		nightlyProfiles = ",CodeCoverage,Nightly"
	}
	timeout(time: 8, unit: 'HOURS') 
	{	
	    def splits = splitTests parallelism: [$class: 'CountDrivenParallelism', size: 3], generateInclusions: true
	    
	    def Groups = [:]
	    echo "Debut Split"
	    for (int i = 0; i < splits.size(); i++) {
	        echo "Split numero &i"   
	        def split = splits[i]
	        
	        Groups["split-${i}"] = {
				node ('citrus && windows7') {
				    deleteDir()
					unstash 'repository'
					dir ('citrus.core')
					{
						coreRoot = pwd()
						unstash 'deltapack_p2'
						unstash 'core_repository'
					}
					dir ('citrus.extensions')
					{
						extensionsRoot = pwd()
						unstash 'extensions_p2'
						unstash 'extensions_maven'
						unstash 'tests'
						unstash 'sigma_product'
					}
					withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
					{
						def SplitMaven = ''
					
						if (split.includes) {
							writeFile file: "Tests/xicdstudio-parallel-test-includes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.includesFile=Tests/xicdstudio-parallel-test-includes-${i}.txt"
						} else {
							writeFile file: "Tests/xicdstudio-parallel-test-excludes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.excludesFile=Tests/xicdstudio-parallel-test-excludes-${i}.txt"
						}
						bat """
							REM Workaround for Windows path length limit of 260 characters
							subst S: /D
							subst S: %WORKSPACE%
							S:
							cd citrus.extensions
							mvn -f Tests/xicdstudio/com.airbus.citrus.xicdstudio.tests.parent/pom.xml clean verify -B -Dmaven.test.failure.ignore -Dcitrus.core.root=S:/citrus.core -Dcitrus.extensions.root=S:/citrus.extensions -PArtal,External${nightlyProfiles} -U ${SplitMaven}
							subst S: /D
						"""
					
						step([$class: 'JUnitResultArchiver', testResults: 'Tests/xicdstudio/**/target/surefire-reports/TEST-*.xml'])
					}
				}
			}
	    }
	    parallel Groups	
	}
}

def validate_xicdstudio_linux(boolean nightly)
{
	def nightlyProfiles = ""
	if (nightly)
	{
		nightlyProfiles = ",CodeCoverage,Nightly"
	}
	timeout(time: 8, unit: 'HOURS') 
	{	
	    def splits = splitTests parallelism: [$class: 'CountDrivenParallelism', size: 3], generateInclusions: true
	    
	    def Groups = [:]
	    
	    for (int i = 0; i < splits.size(); i++) {
	        
	        def split = splits[i]
	        
	        Groups["split-${i}"] = {
				node ('citrus_linux && RHEL6'){
					withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
					{
						def SplitMaven = ''
					
						if (split.includes) {
							writeFile file: "Tests/xicdstudio-parallel-test-includes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.includesFile=Tests/xicdstudio-parallel-test-includes-${i}.txt"
						} else {
							writeFile file: "Tests/xicdstudio-parallel-test-excludes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.excludesFile=Tests/xicdstudio-target/parallel-test-excludes-${i}.txt"
						}
						sh """
							#get first available display
							disp=0
							while [ -e /tmp/.X11-unix/X\$disp ]
							do
								disp=\$((disp+1))
							done
							echo "create and use display \$disp"
							Xvfb :\$disp -screen 0 1920x1080x24 -fbdir /tmp 2> /dev/null	&
							export DISPLAY=:\$disp
							mvn -f Tests/xicdstudio/com.airbus.citrus.xicdstudio.tests.parent/pom.xml clean verify -B -Dmaven.test.failure.ignore -Dcitrus.core.root=${coreRoot} -Dcitrus.extensions.root=${extensionsRoot} -PArtal,External${nightlyProfiles} -U ${SplitMaven}
							find "Tests/xicdstudio/" -name "TEST-*.xml" -exec sed -i \"s/\\(classname=['\\\"]\\)/\\1linux./g\" {} \\;
						"""
						step([$class: 'JUnitResultArchiver', testResults: 'Tests/xicdstudio/**/target/surefire-reports/TEST-*.xml'])
					}
				}
			}
	    }
	    parallel Groups	
	}
}

def validate_connections_windows(boolean nightly)
{
	def nightlyProfiles = ""
	if (nightly)
	{
		nightlyProfiles = ",CodeCoverage,Nightly"
	}
	timeout(time: 8, unit: 'HOURS') 
	{	
	    def splits = splitTests parallelism: [$class: 'CountDrivenParallelism', size: 3], generateInclusions: true
	    
	    def Groups = [:]
	    
	    for (int i = 0; i < splits.size(); i++) {
	        
	        def split = splits[i]
	        
	        Groups["split-${i}"] = {
				node ('citrus && windows7') {
				    deleteDir()
					unstash 'repository'
					dir ('citrus.core')
					{
						coreRoot = pwd()
						unstash 'deltapack_p2'
						unstash 'core_repository'
					}
					dir ('citrus.extensions')
					{
						extensionsRoot = pwd()
						unstash 'extensions_p2'
						unstash 'extensions_maven'
						unstash 'tests'
						unstash 'sigma_product'
					}
					withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
					{
						def SplitMaven = ''
					
						if (split.includes) {
							writeFile file: "Tests/mexicopp-parallel-test-includes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.includesFile=Tests/mexicopp-parallel-test-includes-${i}.txt"
						} else {
							writeFile file: "Tests/mexicopp-parallel-test-excludes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.excludesFile=Tests/mexicopp-parallel-test-excludes-${i}.txt"
						}
						bat """
							REM Workaround for Windows path length limit of 260 characters
							subst S: /D
							subst S: %WORKSPACE%
							S:
							cd citrus.extensions
							mvn -f Tests/mexicopp/com.airbus.citrus.mexicopp.tests.parent/pom.xml clean verify -B -Dmaven.test.failure.ignore -Dcitrus.core.root=S:/citrus.core -Dcitrus.extensions.root=S:/citrus.extensions -PArtal,External${nightlyProfiles} -U ${SplitMaven}
							subst S: /D
						""" 
						step([$class: 'JUnitResultArchiver', testResults: 'Tests/mexicopp/**/target/surefire-reports/TEST-*.xml'])
					}
				}
			}
	    }
	    parallel Groups	
	}
}

def validate_connections_linux(boolean nightly)
{
	def nightlyProfiles = ""
	if (nightly)
	{
		nightlyProfiles = ",CodeCoverage,Nightly"
	}
	timeout(time: 8, unit: 'HOURS') 
	{	
	    def splits = splitTests parallelism: [$class: 'CountDrivenParallelism', size: 3], generateInclusions: true
	    
	    def Groups = [:]
	    
	    for (int i = 0; i < splits.size(); i++) {
	        
	        def split = splits[i]
	        
	        Groups["split-${i}"] = {
				node ('citrus_linux && RHEL6') {
					withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
					{
						def SplitMaven = ''
					
						if (split.includes) {
							writeFile file: "Tests/mexicopp-parallel-test-includes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.includesFile=Tests/mexicopp-parallel-test-includes-${i}.txt"
						} else {
							writeFile file: "Tests/mexicopp-parallel-test-excludes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.excludesFile=Tests/mexicopp-parallel-test-excludes-${i}.txt"
						}
						sh """
							#get first available display
							disp=0
							while [ -e /tmp/.X11-unix/X\$disp ]
							do
								disp=\$((disp+1))
							done
							echo "create and use display \$disp"
							Xvfb :\$disp -screen 0 1920x1080x24 -fbdir /tmp 2> /dev/null	&
							export DISPLAY=:\$disp
							mvn -f Tests/mexicopp/com.airbus.citrus.mexicopp.tests.parent/pom.xml clean verify -B -Dmaven.test.failure.ignore -Dcitrus.core.root=${coreRoot} -Dcitrus.extensions.root=${extensionsRoot} -PArtal,External${nightlyProfiles} -U ${SplitMaven}
							find "Tests/mexicopp/" -name "TEST-*.xml" -exec sed -i \"s/\\(classname=['\\\"]\\)/\\1linux./g\" {} \\;
						"""
						step([$class: 'JUnitResultArchiver', testResults: 'Tests/mexicopp/**/target/surefire-reports/TEST-*.xml'])
					}
				}
			}
	    }
	    parallel Groups	
	}
}

def validate_workman_gui_windows(boolean nightly)
{
	def nightlyProfiles = ""
	if (nightly)
	{
		nightlyProfiles = ",CodeCoverage,Nightly"
	}
	timeout(time: 8, unit: 'HOURS') 
	{	
	    def splits = splitTests parallelism: [$class: 'CountDrivenParallelism', size: 3], generateInclusions: true
	    
	    def Groups = [:]
	    
	    for (int i = 0; i < splits.size(); i++) {
	        
	        def split = splits[i]
	        
	        Groups["split-${i}"] = {
				node ('citrus && windows7') {
				    deleteDir()
					unstash 'repository'
					dir ('citrus.core')
					{
						coreRoot = pwd()
						unstash 'deltapack_p2'
						unstash 'core_repository'
					}
					dir ('citrus.extensions')
					{
						extensionsRoot = pwd()
						unstash 'extensions_p2'
						unstash 'extensions_maven'
						unstash 'tests'
						unstash 'sigma_product'
					}
					withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
					{
						def SplitMaven = ''
					
						if (split.includes) {
							writeFile file: "Tests/target-workman-parallel-test-includes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.includesFile=Tests/target-workman-parallel-test-includes-${i}.txt"
						} else {
							writeFile file: "Tests/target-workman-parallel-test-excludes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.excludesFile=Tests/target-workman-parallel-test-excludes-${i}.txt"
						}
						bat """
							REM Workaround for Windows path length limit of 260 characters
							subst S: /D
							subst S: %WORKSPACE%
							S:
							cd citrus.extensions
							call mvn -f Tests/com.airbus.citrus.tests.prepare/pom.xml clean verify
							call mvn -f Tests/com.airbus.citrus.workman.rcptt.test/pom.xml clean verify -B -Dmaven.test.failure.ignore -Dplatform=win32.win32.x86_64 -DtestSuite=GlobalTest ${SplitMaven}
							cd %WORKSPACE%
							subst S: /D
						"""
						
						archive_results()
						step([$class: 'JUnitResultArchiver', testResults: 'Tests/target-workman*/surefire-reports/TEST_*.xml'])
					}
				}
			}
	    }
	    parallel Groups	
	}
}

def validate_workman_gui_linux(boolean nightly)
{
	echo "TODO: workman_gui_linux"
}

def validate_workman_cli_windows(boolean nightly)
{
	def nightlyProfiles = ""
	if (nightly)
	{
		nightlyProfiles = ",CodeCoverage,Nightly"
	}
	timeout(time: 8, unit: 'HOURS') 
	{	
	    def splits = splitTests parallelism: [$class: 'CountDrivenParallelism', size: 3], generateInclusions: true
	    
	    def Groups = [:]
	    
	    for (int i = 0; i < splits.size(); i++) {
	        
	        def split = splits[i]
	        
	        Groups["split-${i}"] = {
				node ('citrus && windows7') {
				    deleteDir()
					unstash 'repository'
					dir ('citrus.core')
					{
						coreRoot = pwd()
						unstash 'deltapack_p2'
						unstash 'core_repository'
					}
					dir ('citrus.extensions')
					{
						extensionsRoot = pwd()
						unstash 'extensions_p2'
						unstash 'extensions_maven'
						unstash 'tests'
						unstash 'sigma_product'
					}
					withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
					{
						def SplitMaven = ''
					
						if (split.includes) {
							writeFile file: "Tests/workman-cli-parallel-test-includes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.includesFile=Tests/workman-cli-parallel-test-includes-${i}.txt"
						} else {
							writeFile file: "Tests/workman-cli-parallel-test-excludes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.excludesFile=Tests/workman-cli-parallel-test-excludes-${i}.txt"
						}
						bat """
							REM Workaround for Windows path length limit of 260 characters
							subst S: /D
							subst S: %WORKSPACE%
							S:
							cd citrus.extensions
							mvn -f Tests/com.airbus.citrus.workman.cli.test/pom.xml clean verify -B -Dmaven.test.failure.ignore -Dauto_test ${SplitMaven}
							cd %WORKSPACE%
							subst S: /D
						"""
						archive_results()
						step([$class: 'JUnitResultArchiver', testResults: 'Tests/com.airbus.citrus.workman.cli.test/target/surefire-reports/TEST-*.xml'])
					}
				}
			}
	    }
	    parallel Groups	
	}
}

def validate_workman_cli_linux(boolean nightly)
{
	def nightlyProfiles = ""
	if (nightly)
	{
		nightlyProfiles = ",CodeCoverage,Nightly"
	}
	timeout(time: 8, unit: 'HOURS') 
	{	
	    def splits = splitTests parallelism: [$class: 'CountDrivenParallelism', size: 3], generateInclusions: true
	    
	    def Groups = [:]
	    
	    for (int i = 0; i < splits.size(); i++) {
	        
	        def split = splits[i]
	        
	        Groups["split-${i}"] = {
				node ('citrus_linux && RHEL6'){
					withMaven(jdk: 'JDK_8', maven: 'MAVEN_3.3', mavenLocalRepo: '${WORKSPACE}/.repository', mavenOpts: '-Xms512m -Xmx2048m', mavenSettingsConfig: 'cdfe574a-45dd-44d3-8faf-7533385bd7dd', options: [artifactsPublisher(disabled: true)]) 
					{
						def SplitMaven = ''
					
						if (split.includes) {
							writeFile file: "Tests/workman-cli-parallel-test-includes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.includesFile=Tests/workman-cli-parallel-test-includes-${i}.txt"
						} else {
							writeFile file: "Tests/workman-cli-parallel-test-excludes-${i}.txt", text: split.list.join("\n")
							SplitMaven += " -Dsurefire.excludesFile=Tests/workman-cli-parallel-test-excludes-${i}.txt"
						}
						sh '''
							#get first available display
							disp=0
							while [ -e /tmp/.X11-unix/X$disp ]
							do
								disp=$((disp+1))
							done
				
							echo "create and use display $disp"
				
							Xvfb :$disp -screen 0 1280x720x24 -fbdir /tmp 2> /dev/null	&
							export DISPLAY=:$disp
							find . -name "*.bat" -exec chmod +x {} \\; -exec dos2unix {} \\;
							mvn -f Tests/com.airbus.citrus.workman.cli.test/pom.xml clean verify -B -Dmaven.test.failure.ignore ${SplitMaven}
							find "Tests/com.airbus.citrus.workman.cli.test/" -name "TEST-*.xml" -exec sed -i \"s/\\(classname=['\\\"]\\)/\\1linux./g\" {} \\;
						'''
						archive_results()
						step([$class: 'JUnitResultArchiver', testResults: 'Tests/com.airbus.citrus.workman.cli.test/target/surefire-reports/TEST-*.xml'])
					}
				}
			}
	    }
	    parallel Groups	
	}
}

return this;
