var GaussianNB = function(priors, sigmas, thetas) {

    this.priors = priors;
    this.sigmas = sigmas;
    this.thetas = thetas;

    this.predict = function(features) {
        var likelihoods = new Array(this.sigmas.length);
    
        for (var i = 0, il = this.sigmas.length; i < il; i++) {
            var sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.log(2. * Math.PI * this.sigmas[i][j]);
            }
            var nij = -0.5 * sum;
            sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.pow(features[j] - this.thetas[i][j], 2.) / this.sigmas[i][j];
            }
            nij -= 0.5 * sum;
            likelihoods[i] = Math.log(this.priors[i]) + nij;
        }
    
        var classIdx = 0;
        for (var i = 0, l = likelihoods.length; i < l; i++) {
            classIdx = likelihoods[i] > likelihoods[classIdx] ? i : classIdx;
        }
        return classIdx;
    };

};

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv.length - 2 === 8) {

        // Features:
        var features = process.argv.slice(2);

        // Parameters:
        var priors = [0.5055702011935848, 0.4944297988064152];
        var sigmas = [[1.5429539706608868, 0.517629468368873, 1.000000000005888e-09, 4.096450011330212e-05, 1.9748332973049765, 0.08328144739999378, 1.5622345577802794, 0.7305398631109764], [0.35234626954857, 1.428507760171025, 2.0222912150677903, 2.022484559243942, 0.000261920339926264, 1.6940097562894632, 0.4241931059990395, 1.1577498177026868]];
        var thetas = [[-0.21144868537727957, -0.17691782842575296, -0.0107861269516456, -0.001611927316645299, 0.037704125342953594, -0.34303796746743126, 0.02090928921321457, -0.2386453084842271], [0.21621300873515434, 0.18090410878891441, 0.011029158004275928, 0.0016482469700434645, -0.03855366784381681, 0.3507672366189786, -0.02138041351852997, 0.2440224212129811]];

        // Estimator:
        var clf = new GaussianNB(priors, sigmas, thetas);
        var prediction = clf.predict(features);
        console.log(prediction);

    }
}