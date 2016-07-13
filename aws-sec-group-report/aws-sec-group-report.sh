export JAVA_HOME=/usr/lib/jvm/jre
export EC2_HOME=/opt/ec2-api-tools-1.7.5.1

sgdump='/opt/ec2-api-tools-1.7.5.1/bin/ec2-describe-group'
key='' 
secret=''

header='SecurityGroup,Protocol,PortRangeFrom,PortRangeTo,Flow,Source/Destination,SourceID/DestinationID' 

cidr_sg=()
while read i

	do

#		echo $i
		cidr_sg+=( "$i" )

	done < <(
			${sgdump} -O ${key} -W ${secret} --hide-tags --show-empty-fields --region eu-west-1 | \
			awk -v OFS=',' '$1 ~ /^ *PERMISSION*/ && ($3 ~ /^ *PROD*/ || $3 ~ /^ *PRD*/) && ($9 ~ /^ *CIDR*/) {print $3,$5,$6,$7,$11,$10}'
		)

user_sg_init=()
while read i

	do

#		echo $i
		user_sg_init+=( "$i" )

	done < <(
			${sgdump} -O ${key} -W ${secret} --hide-tags --show-empty-fields --region eu-west-1 | \
			awk -v OFS=',' '$1 ~ /^ *PERMISSION*/ && ($3 ~ /^ *PROD*/ || $3 ~ /^ *PRD*/) && ($9 ~ /^ *USER*/) {print $3,$5,$6,$7,$14}'
		)

user_srcsid=()
while read i

	do
	
#		echo $i	
		user_srcsid+=( "$i" )
	
	done < <( 
			${sgdump} -O ${key} -W ${secret} --hide-tags --show-empty-fields --region eu-west-1 | \
			awk '$1 ~ /^ *PERMISSION*/ && ($3 ~ /^ *PROD*/ || $3 ~ /^ *PRD*/) && ($9 ~ /^ *USER*/) {print $13}' 
		)


user_srcname=()
while read i

	do

#		echo $i
		user_srcname+=( "$i" )

	done < <( 
			for i in ${user_srcsid[@]}

				do
				
					${sgdump} -O ${key} -W ${secret} --hide-tags --show-empty-fields --region eu-west-1 $i | awk '$1 ~ /^ *GROUP*/ {print $4}'
				
				done 
		)


user_sg=()
while read i

	do

#		echo $i
		user_sg+=( "$i" )

	done < <(

			array_el=0
			while [ ${array_el} -lt ${#user_sg_init[@]} ] && [ ${array_el} -lt ${#user_srcname[@]} ] && [ ${array_el} -lt ${#user_srcsid[@]} ];

				do

					echo "${user_sg_init[$array_el]},${user_srcname[$array_el]},${user_srcsid[$array_el]}"
					(( array_el++ ))

				done
		)

#echo ${#user_sg_init[@]}
#echo ${#user_srcname[@]}
#echo ${#user_srcsid[@]}
#echo ${#cidr_sg[@]}
#echo ${#user_sg[@]}

draft=()
draft+=( "${cidr_sg[@]}" )
draft+=( "${user_sg[@]}" )

report=( $( printf "%s\n" "${draft[@]}" | sort ) )

echo $header > /tmp/sgdump

for i in ${report[@]}

	do

		echo $i >> /tmp/sgdump

	done
